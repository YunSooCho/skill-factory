"""
Dify API - AI Workflow Platform Client

Supports:
- Create Document from Text
- Update Knowledge Base
- Execute Workflow
- Get Dataset Details
- Send Chat Message
- Get Knowledge Base Tags
- List Datasets
- Upload File for Workflow
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Document:
    """Document representation"""
    id: str
    name: str
    content: str
    created_at: str
    updated_at: str


@dataclass
class CreateDocumentResponse:
    """Document creation response"""
    document: Document
    success: bool
    message: str


@dataclass
class KnowledgeBase:
    """Knowledge base information"""
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str
    document_count: int


@dataclass
class UpdateKnowledgeBaseResponse:
    """Knowledge base update response"""
    knowledge_base: KnowledgeBase
    success: bool
    message: str


@dataclass
class WorkflowExecution:
    """Workflow execution result"""
    execution_id: str
    status: str
    result: Dict[str, Any]
    error: Optional[str]


@dataclass
class ExecuteWorkflowResponse:
    """Workflow execution response"""
    execution: WorkflowExecution
    success: bool
    message: str


@dataclass
class Dataset:
    """Dataset information"""
    id: str
    name: str
    description: str
    document_count: int
    created_at: str


@dataclass
class DatasetDetailsResponse:
    """Dataset details response"""
    dataset: Dataset
    documents: List[Document]
    total: int


@dataclass
class ChatMessage:
    """Chat message"""
    id: str
    role: str
    content: str
    created_at: str


@dataclass
class ChatResponse:
    """Chat response"""
    message: ChatMessage
    conversation_id: str
    success: bool


@dataclass
class Tag:
    """Knowledge base tag"""
    id: str
    name: str
    color: Optional[str]


@dataclass
class GetTagsResponse:
    """Knowledge base tags response"""
    tags: List[Tag]
    total: int


@dataclass
class ListDatasetsResponse:
    """Datasets list response"""
    datasets: List[Dataset]
    total: int
    page: int
    page_size: int


@dataclass
class FileUpload:
    """Uploaded file information"""
    id: str
    name: str
    size: int
    url: str
    created_at: str


@dataclass
class UploadFileResponse:
    """File upload response"""
    file: FileUpload
    success: bool
    message: str


class DifyAPIClient:
    """
    Dify API client for AI workflow platform.

    API Documentation: https://docs.dify.ai/
    """

    BASE_URL = "https://api.dify.ai/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Dify API client.

        Args:
            api_key: Dify API key
            base_url: Custom base URL (optional)
        """
        self.api_key = api_key
        self.BASE_URL = base_url or self.BASE_URL
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_document_from_text(
        self,
        knowledge_base_id: str,
        text: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CreateDocumentResponse:
        """
        Create a document from text content.

        Args:
            knowledge_base_id: Knowledge base ID
            text: Document text content
            name: Document name
            metadata: Optional metadata dictionary

        Returns:
            CreateDocumentResponse with created document

        Raises:
            ValueError: If required fields are missing
            aiohttp.ClientError: If request fails
        """
        if not knowledge_base_id:
            raise ValueError("Knowledge base ID cannot be empty")
        if not text:
            raise ValueError("Text content cannot be empty")
        if not name:
            raise ValueError("Document name cannot be empty")

        payload = {
            "knowledge_base_id": knowledge_base_id,
            "text": text,
            "name": name
        }

        if metadata:
            payload["metadata"] = metadata

        async with self.session.post(
            f"{self.BASE_URL}/documents/text",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Create Document error: {error_msg}")

            doc_data = data.get("document", {})
            document = Document(
                id=doc_data.get("id", ""),
                name=doc_data.get("name", ""),
                content=doc_data.get("content", ""),
                created_at=doc_data.get("created_at", ""),
                updated_at=doc_data.get("updated_at", "")
            )

            return CreateDocumentResponse(
                document=document,
                success=data.get("success", False),
                message=data.get("message", "")
            )

    async def update_knowledge_base(
        self,
        knowledge_base_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> UpdateKnowledgeBaseResponse:
        """
        Update knowledge base information.

        Args:
            knowledge_base_id: Knowledge base ID
            name: Optional new name
            description: Optional new description

        Returns:
            UpdateKnowledgeBaseResponse with updated knowledge base

        Raises:
            ValueError: If knowledge_base_id is empty
            aiohttp.ClientError: If request fails
        """
        if not knowledge_base_id:
            raise ValueError("Knowledge base ID cannot be empty")

        payload = {"knowledge_base_id": knowledge_base_id}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        async with self.session.put(
            f"{self.BASE_URL}/knowledge-bases/{knowledge_base_id}",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Update Knowledge Base error: {error_msg}")

            kb_data = data.get("knowledge_base", {})
            knowledge_base = KnowledgeBase(
                id=kb_data.get("id", ""),
                name=kb_data.get("name", ""),
                description=kb_data.get("description", ""),
                created_at=kb_data.get("created_at", ""),
                updated_at=kb_data.get("updated_at", ""),
                document_count=kb_data.get("document_count", 0)
            )

            return UpdateKnowledgeBaseResponse(
                knowledge_base=knowledge_base,
                success=data.get("success", False),
                message=data.get("message", "")
            )

    async def execute_workflow(
        self,
        workflow_id: str,
        inputs: Dict[str, Any],
        user: str = "default"
    ) -> ExecuteWorkflowResponse:
        """
        Execute a workflow.

        Args:
            workflow_id: Workflow ID
            inputs: Input parameters for the workflow
            user: User identifier (default: "default")

        Returns:
            ExecuteWorkflowResponse with execution result

        Raises:
            ValueError: If required fields are missing
            aiohttp.ClientError: If request fails
        """
        if not workflow_id:
            raise ValueError("Workflow ID cannot be empty")
        if not inputs:
            raise ValueError("Inputs cannot be empty")

        payload = {
            "workflow_id": workflow_id,
            "inputs": inputs,
            "user": user
        }

        async with self.session.post(
            f"{self.BASE_URL}/workflows/run",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Execute Workflow error: {error_msg}")

            execution_data = data.get("execution", {})
            execution = WorkflowExecution(
                execution_id=execution_data.get("id", ""),
                status=execution_data.get("status", ""),
                result=execution_data.get("result", {}),
                error=execution_data.get("error")
            )

            return ExecuteWorkflowResponse(
                execution=execution,
                success=data.get("success", False),
                message=data.get("message", "")
            )

    async def get_dataset_details(
        self,
        dataset_id: str
    ) -> DatasetDetailsResponse:
        """
        Get detailed information about a dataset.

        Args:
            dataset_id: Dataset ID

        Returns:
            DatasetDetailsResponse with dataset and documents

        Raises:
            ValueError: If dataset_id is empty
            aiohttp.ClientError: If request fails
        """
        if not dataset_id:
            raise ValueError("Dataset ID cannot be empty")

        async with self.session.get(
            f"{self.BASE_URL}/datasets/{dataset_id}"
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Get Dataset error: {error_msg}")

            dataset_data = data.get("dataset", {})
            dataset = Dataset(
                id=dataset_data.get("id", ""),
                name=dataset_data.get("name", ""),
                description=dataset_data.get("description", ""),
                document_count=dataset_data.get("document_count", 0),
                created_at=dataset_data.get("created_at", "")
            )

            documents = [
                Document(
                    id=doc.get("id", ""),
                    name=doc.get("name", ""),
                    content=doc.get("content", ""),
                    created_at=doc.get("created_at", ""),
                    updated_at=doc.get("updated_at", "")
                )
                for doc in data.get("documents", [])
            ]

            return DatasetDetailsResponse(
                dataset=dataset,
                documents=documents,
                total=len(documents)
            )

    async def send_chat_message(
        self,
        chat_id: str,
        message: str,
        user: str = "default",
        conversation_id: Optional[str] = None
    ) -> ChatResponse:
        """
        Send a chat message to an AI assistant.

        Args:
            chat_id: Chat bot ID
            message: User message
            user: User identifier (default: "default")
            conversation_id: Optional conversation ID for context

        Returns:
            ChatResponse with assistant message

        Raises:
            ValueError: If required fields are missing
            aiohttp.ClientError: If request fails
        """
        if not chat_id:
            raise ValueError("Chat ID cannot be empty")
        if not message:
            raise ValueError("Message cannot be empty")

        payload = {
            "chat_id": chat_id,
            "message": message,
            "user": user
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        async with self.session.post(
            f"{self.BASE_URL}/chat-messages",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Chat error: {error_msg}")

            msg_data = data.get("message", {})
            message_obj = ChatMessage(
                id=msg_data.get("id", ""),
                role=msg_data.get("role", ""),
                content=msg_data.get("content", ""),
                created_at=msg_data.get("created_at", "")
            )

            return ChatResponse(
                message=message_obj,
                conversation_id=data.get("conversation_id", ""),
                success=data.get("success", False)
            )

    async def get_knowledge_base_tags(
        self,
        knowledge_base_id: str
    ) -> GetTagsResponse:
        """
        Get all tags for a knowledge base.

        Args:
            knowledge_base_id: Knowledge base ID

        Returns:
            GetTagsResponse with list of tags

        Raises:
            ValueError: If knowledge_base_id is empty
            aiohttp.ClientError: If request fails
        """
        if not knowledge_base_id:
            raise ValueError("Knowledge base ID cannot be empty")

        async with self.session.get(
            f"{self.BASE_URL}/knowledge-bases/{knowledge_base_id}/tags"
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Get Tags error: {error_msg}")

            tags = [
                Tag(
                    id=t.get("id", ""),
                    name=t.get("name", ""),
                    color=t.get("color")
                )
                for t in data.get("tags", [])
            ]

            return GetTagsResponse(
                tags=tags,
                total=len(tags)
            )

    async def list_datasets(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> ListDatasetsResponse:
        """
        List all datasets.

        Args:
            page: Page number (default: 1)
            page_size: Items per page (default: 20)

        Returns:
            ListDatasetsResponse with list of datasets

        Raises:
            aiohttp.ClientError: If request fails
        """
        params = {
            "page": page,
            "page_size": page_size
        }

        async with self.session.get(
            f"{self.BASE_URL}/datasets",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify List Datasets error: {error_msg}")

            datasets = [
                Dataset(
                    id=d.get("id", ""),
                    name=d.get("name", ""),
                    description=d.get("description", ""),
                    document_count=d.get("document_count", 0),
                    created_at=d.get("created_at", "")
                )
                for d in data.get("datasets", [])
            ]

            return ListDatasetsResponse(
                datasets=datasets,
                total=data.get("total", len(datasets)),
                page=page,
                page_size=page_size
            )

    async def upload_file_for_workflow(
        self,
        file_path: str,
        workflow_id: str
    ) -> UploadFileResponse:
        """
        Upload a file for workflow use.

        Args:
            file_path: Path to file to upload
            workflow_id: Workflow ID

        Returns:
            UploadFileResponse with uploaded file information

        Raises:
            ValueError: If file not found or workflow_id empty
            aiohttp.ClientError: If request fails
        """
        import os

        if not workflow_id:
            raise ValueError("Workflow ID cannot be empty")
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        # Read file
        with open(file_path, "rb") as f:
            file_data = f.read()

        filename = os.path.basename(file_path)

        data = aiohttp.FormData()
        data.add_field("file", file_data, filename=filename)
        data.add_field("workflow_id", workflow_id)

        async with self.session.post(
            f"{self.BASE_URL}/files/upload",
            data=data
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("message", str(data))
                raise Exception(f"Dify Upload File error: {error_msg}")

            file_data = data.get("file", {})
            file = FileUpload(
                id=file_data.get("id", ""),
                name=file_data.get("name", ""),
                size=file_data.get("size", 0),
                url=file_data.get("url", ""),
                created_at=file_data.get("created_at", "")
            )

            return UploadFileResponse(
                file=file,
                success=data.get("success", False),
                message=data.get("message", "")
            )


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with DifyAPIClient(api_key) as client:
        # List datasets
        datasets = await client.list_datasets(page=1, page_size=10)
        print(f"Found {datasets.total} datasets")
        for dataset in datasets.datasets[:3]:
            print(f"  - {dataset.name} ({dataset.document_count} documents)")

        # Send chat message
        chat_result = await client.send_chat_message(
            chat_id="your-chat-id",
            message="Hello! How can you help me today?"
        )
        print(f"Chat response: {chat_result.message.content}")

        # Execute workflow
        workflow_result = await client.execute_workflow(
            workflow_id="your-workflow-id",
            inputs={"query": "What is AI?"},
            user="test-user"
        )
        print(f"Workflow status: {workflow_result.execution.status}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())