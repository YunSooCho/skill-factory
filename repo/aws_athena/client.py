"""
AWS Athena API Client

This module provides a Python client for interacting with AWS Athena.
"""

import boto3
import time
from typing import Dict, List, Optional, Any, Iterator
from botocore.exceptions import ClientError


class AthenaClient:
    """
    Client for AWS Athena Interactive Query Service.

    Athena provides:
    - Serverless SQL queries on S3 data
    - Standard SQL support
    - Serverless architecture with no infrastructure to manage
    - Integration with AWS Glue Data Catalog
    """

    def __init__(
        self,
        region_name: str,
        output_location: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        s3_staging_dir: Optional[str] = None,
        workgroup: Optional[str] = None
    ):
        """Initialize the Athena client."""
        session_config = {'region_name': region_name}
        if aws_access_key_id and aws_secret_access_key:
            session_config.update({
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key
            })

        self.session = boto3.client('athena', **session_config)
        self.s3_client = boto3.client('s3', **session_config) if s3_staging_dir else None
        self.output_location = output_location
        self.s3_staging_dir = s3_staging_dir
        self.workgroup = workgroup

    def start_query_execution(
        self,
        query_string: str,
        database: Optional[str] = None,
        query_execution_context: Optional[Dict[str, Any]] = None,
        result_configuration: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a query execution."""
        config = {
            'QueryString': query_string,
            'ResultConfiguration': result_configuration or {'OutputLocation': self.output_location}
        }

        if database:
            config['QueryExecutionContext'] = {'Database': database}
        elif query_execution_context:
            config['QueryExecutionContext'] = query_execution_context

        if self.workgroup:
            config['WorkGroup'] = self.workgroup

        response = self.session.start_query_execution(**config)
        return response['QueryExecutionId']

    def get_query_execution(self, query_execution_id: str) -> Dict[str, Any]:
        """Get details of a query execution."""
        response = self.session.get_query_execution(QueryExecutionId=query_execution_id)
        return response['QueryExecution']

    def get_query_results(
        self,
        query_execution_id: str,
        max_results: int = 1000,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get query results."""
        params = {'QueryExecutionId': query_execution_id, 'MaxResults': max_results}
        if next_token:
            params['NextToken'] = next_token

        response = self.session.get_query_results(**params)
        return {
            'rows': response['ResultSet']['Rows'],
            'next_token': response.get('NextToken')
        }

    def wait_for_query_completion(
        self,
        query_execution_id: str,
        check_interval: float = 1.0,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Wait for a query to complete."""
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Query {query_execution_id} timed out")

            execution = self.get_query_execution(query_execution_id)
            state = execution['Status']['State']

            if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                return execution

            time.sleep(check_interval)

    def execute_query(
        self,
        query_string: str,
        database: Optional[str] = None,
        wait: bool = True,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Execute a query and optionally wait for completion."""
        query_id = self.start_query_execution(query_string, database)

        if wait:
            execution = self.wait_for_query_completion(query_id, timeout=timeout)

            if execution['Status']['State'] != 'SUCCEEDED':
                raise Exception(
                    f"Query failed: {execution['Status']['StateChangeReason']}"
                )

            results = self.get_query_results(query_id)
            return {
                'query_execution_id': query_id,
                'execution': execution,
                'results': results
            }

        return {'query_execution_id': query_id}

    def query_to_dataframe(
        self,
        query_string: str,
        database: Optional[str] = None,
        timeout: int = 300
    ):
        """Execute query and return pandas DataFrame."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for query_to_dataframe")

        result = self.execute_query(query_string, database, timeout=timeout)

        # Extract column names
        columns = [col['VarCharValue'] for col in result['results']['rows'][0]['Data']]

        # Extract data rows
        rows = [
            [cell.get('VarCharValue', '') for cell in row['Data']]
            for row in result['results']['rows'][1:]
        ]

        return pd.DataFrame(rows, columns=columns)

    def get_all_query_results(self, query_execution_id: str) -> List[Dict[str, Any]]:
        """Get all results with pagination."""
        all_rows = []
        next_token = None

        while True:
            result = self.get_query_results(query_execution_id, next_token=next_token)
            all_rows.extend(result['rows'])

            if not result['next_token']:
                break

            next_token = result['next_token']

        return all_rows

    def list_databases(self, max_results: int = 50) -> List[str]:
        """List databases in Athena."""
        response = self.session.list_databases(MaxResults=max_results)
        return [db['Name'] for db in response['DatabaseList']]

    def list_tables(
        self,
        database: str,
        max_results: int = 50,
        catalog_name: str = 'awsdatacatalog'
    ) -> List[Dict[str, Any]]:
        """List tables in a database."""
        response = self.session.list_table_metadata(
            CatalogName=catalog_name,
            DatabaseName=database,
            MaxResults=max_results
        )
        return response['TableMetadataList']

    def get_table_metadata(
        self,
        database: str,
        table: str,
        catalog_name: str = 'awsdatacatalog'
    ) -> Dict[str, Any]:
        """Get table metadata."""
        response = self.session.get_table_metadata(
            CatalogName=catalog_name,
            DatabaseName=database,
            TableName=table
        )
        return response['TableMetadata']

    def create_database(self, database: str) -> str:
        """Create a new database."""
        response = self.session.start_query_execution(
            QueryString=f"CREATE DATABASE IF NOT EXISTS {database}",
            ResultConfiguration={'OutputLocation': self.output_location}
        )
        return response['QueryExecutionId']

    def drop_database(self, database: str) -> str:
        """Drop a database."""
        response = self.session.start_query_execution(
            QueryString=f"DROP DATABASE IF EXISTS {database}",
            ResultConfiguration={'OutputLocation': self.output_location}
        )
        return response['QueryExecutionId']

    def cancel_query(self, query_execution_id: str) -> None:
        """Cancel a running query."""
        self.session.stop_query_execution(QueryExecutionId=query_execution_id)

    def batch_query(
        self,
        queries: List[str],
        database: Optional[str] = None,
        parallel: int = 5
    ) -> List[Dict[str, Any]]:
        """Execute multiple queries in parallel."""
        import concurrent.futures

        def run_query(query: str) -> Dict[str, Any]:
            return self.execute_query(query, database)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {executor.submit(run_query, query): query for query in queries}
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({'error': str(e), 'query': futures[future]})

        return results

    def get_query_history(
        self,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """Get query execution history."""
        response = self.session.list_query_executions(MaxResults=max_results)
        return response['QueryExecutionIds']

    def export_results_to_s3(
        self,
        query_execution_id: str,
        bucket: str,
        key: str,
        format: str = 'csv'
    ) -> str:
        """Export query results to S3 in specified format."""
        if not self.s3_client:
            raise ValueError("S3 client not initialized. Provide s3_staging_dir parameter.")

        results = self.get_all_query_results(query_execution_id)

        if format == 'csv':
            try:
                import csv
                import io

                output = io.StringIO()
                columns = [cell.get('VarCharValue', '') for cell in results[0]['Data']]
                writer = csv.DictWriter(output, fieldnames=columns)
                writer.writeheader()

                for row in results[1:]:
                    row_dict = {
                        col: cell.get('VarCharValue', '')
                        for col, cell in zip(columns, row['Data'])
                    }
                    writer.writerow(row_dict)

                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=output.getvalue()
                )
            except ImportError:
                raise ImportError("CSV export requires Python csv module")

        elif format == 'json':
            import json

            columns = [cell.get('VarCharValue', '') for cell in results[0]['Data']]
            data = []

            for row in results[1:]:
                row_dict = {
                    col: cell.get('VarCharValue', '')
                    for col, cell in zip(columns, row['Data'])
                }
                data.append(row_dict)

            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(data, indent=2)
            )

        return f"s3://{bucket}/{key}"

    def list_named_queries(self) -> List[Dict[str, Any]]:
        """List named queries (saved queries)."""
        response = self.session.list_named_queries()
        return response.get('NamedQueryIds', [])

    def create_named_query(
        self,
        name: str,
        database: str,
        query_string: str,
        description: Optional[str] = None
    ) -> str:
        """Create a named query."""
        params = {
            'Name': name,
            'Database': database,
            'QueryString': query_string
        }
        if description:
            params['Description'] = description

        response = self.session.create_named_query(**params)
        return response['NamedQueryId']

    def get_named_query(self, query_id: str) -> Dict[str, Any]:
        """Get named query details."""
        response = self.session.get_named_query(NamedQueryId=query_id)
        return response['NamedQuery']

    def delete_named_query(self, query_id: str) -> None:
        """Delete a named query."""
        self.session.delete_named_query(NamedQueryId=query_id)

    def get_workgroups(self) -> List[Dict[str, Any]]:
        """List workgroups."""
        response = self.session.list_work_groups()
        return response['WorkGroups']

    def create_workgroup(
        self,
        name: str,
        configuration: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> None:
        """Create a workgroup."""
        params = {'Name': name}
        if configuration:
            params['Configuration'] = configuration
        if description:
            params['Description'] = description

        self.session.create_work_group(**params)

    def delete_workgroup(self, name: str) -> None:
        """Delete a workgroup."""
        self.session.delete_work_group(WorkGroup=name)

    def get_data_catalog(
        self,
        database: Optional[str] = None,
        catalog_name: str = 'awsdatacatalog'
    ) -> Dict[str, Any]:
        """Get data catalog structure."""
        if database:
            tables = self.list_tables(database, catalog_name=catalog_name)
            return {
                'catalog': catalog_name,
                'database': database,
                'tables': tables
            }
        else:
            databases = self.list_databases()
            return {
                'catalog': catalog_name,
                'databases': databases
            }