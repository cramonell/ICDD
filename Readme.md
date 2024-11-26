# ICDD Library Usage

The ICDD python library allow its users to create, import and modify ICDD containers. 

## 0. Import ICDD 
```python
from ICDD import *
import uuid
```

## 1. Containers

### 1.1. Import Container

```python
from ICDD import *
import uuid

# Initialize new Container
container = Container()

#open .icdd file. Provide a temporary folder location to decompress the icdd
container.open(icdd_path, temp_folder_path)

```
### 1.2 Access Container data
The `Container` class provides access to several attributes as described below: 
- `Container.address`: The address associated with the container. 
- `Container.checksum`: The checksum value of the container. 
- `Container.checksum_algorithm`: The algorithm used to calculate the checksum. 
- `Container.conformance_indicator`: ICDD-Part1-Container. 
- `Container.creation_date`: The date the container was created. 
- `Container.description`: A description of the container. 
- `Container.documents`: The collection of documents within the container. 
- `Container.linksets`: A collection of linksets within the container. 
- `Container.modification_date`: The date the container was last modified. 
- `Container.name`: The name of the container. 
- `Container.published_by`: The entity that published the container. 
- `Container.user_id`: The ID of the user who created or modified the container. 
- `Container.version_id`: The version identifier of the container. 
- `Container.version_description`: A description of the version of the container. 
- `Container.website`: The URL associated with the container. 


## 2. Documents

### 2.1. Create documents
The ICDD library includes several specialized document classes, as defined in the ICDD standard:
- `FolderDocument`
- `EncryptedDocument`
- `ExternalDocument`
- `InternalDocument`
- `SecuredDocument`

The documents are created as follow:

```python
# Create internal document type
internal_doc = InternalDocument(path="path_to_your_document.ttl", requested=True)

# Create external document type
external_doc = ExternalDocument(url='https://www.example.org/file_url.pdf')

```

### 2.2 Document data
- `Document.path`: The file path of the document.
- `Document.format`: The format of the document.
- `Document.requested`: A boolean indicating if the document was requested.
- `Document.file_type`: The file type based on the file extension.
- `Document.id`: The unique identifier for the document.

Specific subclasses have additional attributes:

- `FolderDocument.folder_name`: The name of the folder containing the document.
- `EncryptedDocument.encryption_algorithm`: The algorithm used to encrypt the document.
- `ExternalDocument.url`: The URL of the external document.
- `InternalDocument.file_name`: The name of the internal file.
- `SecuredDocument.checksum`: The checksum value of the document.
- `SecuredDocument.checksum_algorithm`: The algorithm used to calculate the checksum.

### 2.3. Add Documents to Containers


```python
container.add_document(internal_doc)
container.add_document(external doc)
```


## 3. Link Sets 

A Linkset can be translated as a linkset file within an .icdd container. The following code instance a new Linkset:

```python
linkset = Linkset()
```

### 3.1. Link Elements
Linksets are formed by two Link Elements.Link Elements can be assigned to a full file, or to specific elements within a file. To do the later, different types of Identifiers are supported:

- `URIBasedIdentifier`
- `StringBasedIdentifier`
- `QueryBasedIdentifier`

The following code shows how to create two different link elements, one is whole docuemnt, the other is an element within a Turtle file that is identified with an URI-based identifier:

```python
# Create Identifier
identifier = URIBasedIdentifier(uri='http://example.org/uribasedidentifier')

# Create Link Elements
link_element_1 = LinkElement(document=internal_document, identifier=identifier)
link_element_2 = LinkElement(document=doc)
```
### 3.2. Links

The following code shows how to create a Link, how to access their Link Elements, and how to add Links to Linksets:

```python
# Create new link
link = Link(link_element_1, link_element_2)

# Access first element of the link
first_le = Link.a # = link_element_1
second_le = Link.b # = link_element_2

# Add link to linkset
linkset.add_link(link)
```

### 3.2. Add Linksets to Containers

Once all Links are placed within a Linkset, they can be added to the container. Once the container has all necessary Documents and Linksets, it can be created using the `create()` fucntion:

```python
container.add_linkset(linkset_img)
container.add_linkset(linkset_docs)

## Create the container
path = "desired_container_path"
container.create(path)
```

# Contact
For further assistance, questions, or feedback, you can reach out to us by email to  [carlos.ramonell@upc.edu](mailto:carlos.ramonell@upc.edu)


We appreciate your interest and contributions to the



