from rdflib import Graph, Literal
import os
import uuid
import shutil


# Documents 
class Document:

    def __init__(self, path:str, format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None) -> None:
        self.path = path
        self.format = format
        self.requested = requested
        self.file_type = '.' + path.split('.')[-1]
        if id: self.id =  id
        else: self.id = uuid.uuid4()

        self.attr_frag_map = {
            "address": "address",
            "creationDate": "creation_date",
            "conformanceIndicator": "conformance_indicator",
            "description": "description",
            "filetype" : "file_type",
            "format": "format",
            "modificationDate": "modification_date",
            "name": "name",
            "requested" : "requested",
            "userID": "user_id",
            "versionID": "version_id",
            "versionDescription": "version_description",
            "website": "website"
        }

class FolderDocument(Document):

    def __init__(self, path:str, folder_name: str, format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None) -> None:
        super().__init__(path=path, format = format, requested = requested, id = id)
        self.folder_name = folder_name
        self.attr_frag_map['foldername'] = 'folder_name'

class EncryptedDocument(Document):

    def __init__(self, path:str, encryption_algorithm: str, format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None ) -> None:
        super().__init__(path=path, format = format, requested = requested, id = id)
        self.encryption_algorithm = encryption_algorithm
        self.attr_frag_map['encryptionAlgorithm'] = 'encryption_algorithm'

class ExternalDocument(Document):

    def __init__(self,   url: str, path:str ='/', format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None) -> None:
        super().__init__(path=path, format = format, requested = requested, id = id)
        self.url = url
        self.file_type = '.'+ self.url.split('.')[-1]
        self.attr_frag_map['filetype'] = 'file_type'
        self.attr_frag_map['url'] = 'url'

class InternalDocument(Document):

    def __init__(self,  path:str, format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None) -> None:
        super().__init__(path=path, format = format, requested = requested, id = id)
        self.file_name = path.split('/')[-1].split('.')[0]
        self.attr_frag_map['filename'] = 'file_name'

class SecuredDocument(Document):

    def __init__(self,  path:str, format:str|None = None, requested:bool = False, id: uuid.UUID|str|None = None) -> None:
        super().__init__(path=path, format = format, requested = requested, id = id)
        self.checksum = None
        self.checksum_algorithm =  None
        self.attr_frag_map['checksum'] = 'checksum'
        self.attr_frag_map['checksumAlgorithm'] = 'checksum_algorithm'
        

#links, linksets, link elements and identifiers
class Identifier:

    def __init__(self) -> None:
        self.id = uuid.uuid4()
        self.attr_frag_map = {
            "address": "address",
            "name": "name",
            "website": "website"
        }

class URIBasedIdentifier(Identifier):

    def __init__(self, uri: str) -> None:
        super().__init__()
        self.uri  =  uri
        self.attr_frag_map['uri'] = 'uri'

class StringBasedIdentifier(Identifier):

    def __init__(self, identifier: str, identifier_field: str|None = None) -> None:
        super().__init__()
        self.identifier = identifier
        self.identifier_field = identifier_field
        self.attr_frag_map['identifier'] = 'identifier'
        self.attr_frag_map['identifierField'] = 'identifier_field'

class QueryBasedIdentifier(Identifier):

    def __init__(self, query_language : str, query_exression: str) -> None:
        super().__init__()
        self.query_language = query_language
        self.query_expression = query_exression
        self.attr_frag_map['queryLanguage'] = 'query_language'
        self.attr_frag_map['queryExpression'] = 'query_expression'

class LinkElement:

    def __init__(self, document: Document|None, identifier: Identifier|None= None, id: uuid.UUID|str|None = None) -> None:
        if not id: self.id = uuid.uuid4()
        else: self.id  =  id
        self.document = document
        self.identifier = identifier

class Link:
    import uuid

    def __init__(self, a:LinkElement, b:LinkElement, id: uuid.UUID|str|None = None) -> None:
        if not id: self.id = uuid.uuid4()
        else: self.id  =  id
        self.a = a
        self.b = b

class Linkset:

    def __init__(self, id: uuid.UUID|str|None = None) -> None:

        from rdflib import Graph, URIRef, Namespace, Literal
        import os
        import uuid
        import datetime


        self.links =  []
        self.linkset = Graph()
        if id: self.id =  id
        else: self.id = uuid.uuid4()
        self.linkset_url =  URIRef("./")
        

        #define container namespaces
        self.INST = Namespace(self.linkset_url)
        self.CONTAINER = Namespace('https://standards.iso.org/iso/21597/-1/ed-1/en/Container#')
        self.LINKSET = Namespace("https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#")
        self.XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
        self.RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        self.OWL = Namespace("http://www.w3.org/2002/07/owl#")

        self.linkset.bind('inst', self.INST)
        self.linkset.bind('linkset', self.LINKSET)
        self.linkset.bind('container', self.CONTAINER)
        self.linkset.bind('xsd', self.XSD)
        self.linkset.bind('rdf', self.RDF)
        self.linkset.bind('rdfs', self.RDFS)

    def reset_graph(self):
        self.linkset = Graph()

        self.linkset.bind('inst', self.INST)
        self.linkset.bind('linkset', self.LINKSET)
        self.linkset.bind('container', self.CONTAINER)
        self.linkset.bind('xsd', self.XSD)
        self.linkset.bind('rdf', self.RDF)
        self.linkset.bind('rdfs', self.RDFS)

    def add_link(self, link:Link):
        self.links.append(link)
    
    def serialize(self, path, format):

        for link in self.links:
            self.linkset.add((self.INST[str(link.id)], self.RDF.type, self.LINKSET.Link))
            
            print('creating link: ' + str(link.id))
            # a element
            self.linkset.add((self.INST[str(link.id)], self.LINKSET.hasLinkElement, self.INST[str(link.a.id)] ))
            self.linkset.add((self.INST[str(link.a.id)], self.RDF.type, self.LINKSET.LinkElement  ))
            if link.a.identifier: self.linkset.add((self.INST[str(link.a.id)], self.LINKSET.hasIdentifier, self.INST[str(link.a.identifier.id)]))
            
            if isinstance(link.a.identifier, URIBasedIdentifier ) and  link.a.identifier: 
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.RDF.type, self.LINKSET.URIBasedIdentifier))
                if link.a.identifier: self.linkset.add((self.INST[str(link.a.identifier.id)], self.LINKSET.uri, Literal(link.a.identifier.uri, datatype=self.XSD.anyURI)))
            
            if isinstance(link.a.identifier, StringBasedIdentifier ) and link.a.identifier: 
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.RDF.type, self.LINKSET.StringBasedIdentifier))
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.LINKSET.identifier, Literal(link.a.identifier.identifier, datatype=self.XSD.string)))
                if link.a.identifier.identifier_field: self.linkset.add((self.INST[str(link.a.identifier.id)], self.LINKSET.identifierField, Literal(link.a.identifier.identifier_field, datatype=self.XSD.string)))
            
            if isinstance(link.a.identifier, QueryBasedIdentifier ) and  link.a.identifier: 
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.RDF.type, self.LINKSET.QueryBasedIdentifier))
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.LINKSET.queryLanguage, Literal(link.a.identifier.query_language, datatype=self.XSD.string)))
                self.linkset.add((self.INST[str(link.a.identifier.id)], self.LINKSET.queryExpression, Literal(link.a.identifier.query_expression, datatype=self.XSD.string)))

            if link.a.document: self.linkset.add((self.INST[str(link.a.id)], self.LINKSET.hasDocument, self.INST[str(link.a.document.id)]))

            # b element
            self.linkset.add((self.INST[str(link.id)], self.LINKSET.hasLinkElement, self.INST[str(link.b.id)] ))
            self.linkset.add((self.INST[str(link.b.id)], self.RDF.type, self.LINKSET.LinkElement  ))
            if link.b.identifier: self.linkset.add((self.INST[str(link.b.id)], self.LINKSET.hasIdentifier, self.INST[str(link.b.identifier.id)]))
            
            if isinstance(link.a.identifier, URIBasedIdentifier ) and link.b.identifier: 
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.RDF.type, self.LINKSET.URIBasedIdentifier))
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.LINKSET.uri, Literal(link.b.identifier.uri, datatype=self.XSD.anyURI)))
            
            if isinstance(link.a.identifier, StringBasedIdentifier ) and link.b.identifier:
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.RDF.type, self.LINKSET.StringBasedIdentifier))
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.LINKSET.identifier, Literal(link.b.identifier.identifier, datatype=self.XSD.string)))
                if link.a.identifier.identifier_field: self.linkset.add((self.INST[str(link.b.identifier.id)], self.LINKSET.identifierField, Literal(link.b.identifier.identifier_field, datatype=self.XSD.string)))
            
            if isinstance(link.a.identifier, QueryBasedIdentifier ) and link.b.identifier: 
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.RDF.type, self.LINKSET.QueryBasedIdentifier))
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.LINKSET.queryLanguage, Literal(link.b.identifier.query_language, datatype=self.XSD.string)))
                self.linkset.add((self.INST[str(link.b.identifier.id)], self.LINKSET.queryExpression, Literal(link.b.identifier.query_expression, datatype=self.XSD.string)))
            
            if link.b.document: self.linkset.add((self.INST[str(link.b.id)], self.LINKSET.hasDocument, self.INST[str(link.b.document.id)]))
            
        self.linkset.serialize(path, format = format)


#Container
class Container:

    def  __init__(self,  conformance_indicator = "ICDD-Part1-Container", id:uuid.UUID|str|None = None) -> None:
        from rdflib import Graph, URIRef, Namespace, Literal
        import os
        import uuid
        import datetime
        import shutil

        # Define the main folder name
        if id: self.container_id = str(id)
        else: self.container_id = str(uuid.uuid4())
        self.container_url =  URIRef("./")

        #define container namespaces
        self.INST = Namespace(self.container_url)
        self.CONTAINER = Namespace('https://standards.iso.org/iso/21597/-1/ed-1/en/Container#')
        self.LINKSET = Namespace("https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#")
        self.XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
        self.RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        self.OWL = Namespace("http://www.w3.org/2002/07/owl#")

        # ICDD ontologies
        self.container_ont = Graph()
        self.container_ont.parse('https://standards.iso.org/iso/21597/-1/ed-1/en/Container.rdf')
        self.linkset_ont = Graph()
        self.linkset_ont.parse('https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset.rdf')

        # ICDD graphs
        self.index = Graph()

        # ICDD Container data
        self.address = None
        self.cheksum = None
        self.checksum_algorithm = None
        self.conformance_indicator = conformance_indicator
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.description = None
        self.documents = []
        self.linksets = []
        self.modification_date = None
        self.name = None
        self.published_by = None
        self.user_id = None
        self.version_id = None
        self.version_description = None
        self.website = None
        
        # Bind your custom prefixes
        self.index.bind("container", self.CONTAINER)
        self.index.bind('linkset', self.LINKSET)
        self.index.bind('rdf', self.RDF)
        self.index.bind('rdfs', self.RDFS)
        self.index.bind('owl', self.OWL)
        self.index.bind('xsd', self.XSD)
        self.index.bind('inst', self.INST)

        self._initialize_container()

        self.attr_frag_map = {
            "address": "address",
            "checksum": "checksum",
            "checksumAlgorithm": "checksum_algorithm",
            "creationDate": "creation_date",
            "conformanceIndicator": "conformance_indicator",
            "description": "description",
            "name": "name",
            "modificationDate": "modification_date",
            "publishedBy": "published_by",
            "userID": "user_id",
            "versionID": "version_id",
            "versionDescription": "version_description",
            "website": "website"
        }

    def reset_index_graph(self):
        self.index = Graph()

        # Bind your custom prefixes
        self.index.bind("container", self.CONTAINER)
        self.index.bind('linkset', self.LINKSET)
        self.index.bind('rdf', self.RDF)
        self.index.bind('rdfs', self.RDFS)
        self.index.bind('owl', self.OWL)
        self.index.bind('xsd', self.XSD)
        self.index.bind('inst', self.INST)


    def _initialize_container(self):
        self.index.add((self.container_url, self.RDF.type, self.CONTAINER.ContainerDescription))
        self.index.add((self.container_url, self.CONTAINER.conformanceIndicator, Literal(self.conformance_indicator, datatype=self.XSD.string)))
        if self.description: self.index.add((self.container_url, self.CONTAINER.description, Literal(self.description, datatype=self.XSD.string)))
        if  self.version_description: self.index.add((self.container_url, self.CONTAINER.versionDescription, Literal(self.version_description, datatype=self.XSD.string)))
        if self.version_id: self.index.add((self.container_url, self.CONTAINER.version, Literal(self.version_id, datatype=self.XSD.string)))
        self.index.add((self.container_url, self.CONTAINER.creationDate, Literal(self.creation_date, datatype=self.XSD.dateTime)))

    def add_document(self, document: Document):
        self.documents.append(document)

    def get_document_by_id(self, id: uuid.UUID|str):
        for document in self.documents:
            if str(document.id) == str(id):
                return document

    def add_linkset(self, linkset: Linkset):
        self.linksets.append(linkset)

    def create(self, root_path:str|None = None):
         
        if root_path:
            if not root_path.endswith('/'): root_path+='/'
            main_folder = root_path + self.container_id
        else: main_folder = self.container_id

        # Create the main folder
        os.makedirs(main_folder, exist_ok=True)

        # Create three subfolders within the main folder
        subfolders = ["Ontology resources", "Payload documents", "Payload triples"]
        for subfolder in subfolders:
            os.makedirs(os.path.join(main_folder, subfolder), exist_ok=True)

        self.container_ont.serialize(self.container_id + '/Ontology resources/Container.ttl', format = 'ttl')
        self.linkset_ont.serialize(self.container_id + '/Ontology resources/Linkset.ttl', format = 'ttl')

        # add documents

        for document in self.documents:

            if isinstance(document, FolderDocument):
                self.index.add((self.INST[str(document.id)], self.RDF.type, self.CONTAINER.FolderDocument))
                self.index.add((self.INST[str(document.id)], self.CONTAINER.foldername, Literal(document.folder_name, datatype=self.XSD.string)))

            elif isinstance(document, ExternalDocument):
                self.index.add((self.INST[str(document.id)], self.RDF.type, self.CONTAINER.ExternalDocument))
                self.index.add((self.INST[str(document.id)], self.CONTAINER.url, Literal(document.url, datatype=self.XSD.string)))

            elif isinstance(document, EncryptedDocument):
                self.index.add((self.INST[str(document.id)], self.RDF.type, self.CONTAINER.EncryptedDocument))
                self.index.add((self.INST[str(document.id)], self.CONTAINER.encryptionAlgorithm, Literal(document.encryption_algorithm, datatype=self.XSD.string)))
                shutil.copy(document.path, self.container_id + '/Payload documents')

            elif isinstance(document, InternalDocument):
                self.index.add((self.INST[str(document.id)], self.RDF.type, self.CONTAINER.InternalDocument))
                self.index.add((self.INST[str(document.id)], self.CONTAINER.filename, Literal(document.file_name, datatype=self.XSD.string)))
                shutil.copy(document.path, self.container_id + '/Payload documents')
            
            else:
                self.index.add((self.INST[str(document.id)], self.RDF.type, self.CONTAINER.Document))
                shutil.copy(document.path, self.container_id + '/Payload documents')


            if document.requested: self.index.add((self.INST[str(document.id)], self.CONTAINER.requested, Literal(True, datatype=self.XSD.boolean)))
            else: self.index.add((self.INST[str(document.id)], self.CONTAINER.requested, Literal(False, datatype=self.XSD.boolean)))

            if document.format: self.index.add((self.INST[str(document.id)], self.CONTAINER['format'], Literal(document.format, datatype=self.XSD.string)))
            
            if document.file_type: self.index.add((self.INST[str(document.id)], self.CONTAINER.filetype, Literal(document.file_type, datatype=self.XSD.string)))
            

            self.index.add((self.container_url, self.CONTAINER.containsDocument, self.INST[str(document.id)]))
            self.index.add((self.INST[str(document.id)], self.CONTAINER.belongsToContainer, self.container_url))

        # add linksets
        for linkset in self.linksets:

            self.index.add((self.INST[str(linkset.id)], self.RDF.type, self.CONTAINER.Linkset))
            self.index.add((self.container_url, self.CONTAINER.containsLinkset, self.INST[str(linkset.id)]))
            self.index.add((self.INST[str(linkset.id)], self.CONTAINER.containedInContainer, self.container_url))
            self.index.add((self.INST[str(linkset.id)], self.CONTAINER.filename, Literal(str(linkset.id) +'.ttl', datatype= self.XSD.string)))

            linkset.serialize(self.container_id + '/Payload triples/' + str(linkset.id) +'.ttl', format = 'ttl')
        

        self.index.serialize(self.container_id + '/' + 'index.ttl', format  ='ttl')
        # Create a zip file
        shutil.make_archive(str(self.container_id), 'zip', str(self.container_id))
        # Rename the zip file to have the custom extension
        os.rename(f"{self.container_id}.zip", f"{self.container_id}.icdd")
        
        # Print a success message
        print(f"container created: {main_folder}")

    def open(self, icdd_path:str, temp_path: str|None = None):
        if not temp_path:  temp_path = './' 
        self.id = icdd_path.split('/')[-1].split('.')[0] 
        temp_path += self.id + '/' 

        # unpack the zip file
        shutil.unpack_archive(icdd_path, temp_path, format = 'zip') 

        def get_document(document_uri):
            document_id = document_uri.split('/')[-1]
            
            query = """
            PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 

            SELECT ?attribute ?value
            WHERE {{
                <{}> ?attribute ?value .
            }}""".format(str(document_uri))
            
            type_query = """
            PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  

            SELECT ?type
            WHERE {{
                <{}> rdf:type ?type .
            }}""".format(str(document_uri))

            type_results  =self.index.query(type_query)
            for item in type_results:
                doc_type = item[0].fragment
            
            results = self.index.query(query)
                      
            if doc_type == "FolderDocument":
                document = FolderDocument(path = '', folder_name = '', id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                document.path  = temp_path + 'Payload documents/'+ str(document.folder_name)
                self.add_document(document)
            
            elif doc_type == "EncryptedDocument":
                document = EncryptedDocument(path = '', encryption_algorithm="", id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                document.path  = temp_path + 'Payload documents/'+ str(document_uri.split('/')[-1])
                self.add_document(document)
                
            elif doc_type == "ExternalDocument":
                document = ExternalDocument(url = "", id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                self.add_document(document)

            elif doc_type == "InternalDocument":
                document = InternalDocument(path = '', id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                document.path  = temp_path + 'Payload documents/'+ str(document.file_name) + str(document.file_type)
                self.add_document(document)

            elif doc_type == "SecuredDocument":
                document = SecuredDocument(path = '', id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                document.path  = temp_path + 'Payload documents/'+ str(document_uri.split('/')[-1])
                self.add_document(document)
            
            else:
                document = Document(path='', id=document_id)
                for item in results:
                    if item[0].fragment in document.attr_frag_map.keys():
                        document.__setattr__(document.attr_frag_map[item[0].fragment], item[1].value)
                document.path  = temp_path + 'Payload documents/'+ str(document_uri.split('/')[-1])
                self.add_document(document)
            
            
            
        def get_linkset(linkset_uri):
            linkset_id = linkset_uri.split('/')[-1]
            linkset = Linkset(id = linkset_id )
            # import Linkset graph
            linkset.linkset.parse(temp_path + 'Payload triples/' + linkset_id + '.ttl') #TODO varios formatos

            # find links, link elements and identifiers + attributes
            query= """
            PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 
            PREFIX linkset: <https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

            SELECT ?link ?linkelement  
            WHERE {{
                ?link linkset:hasLinkElement ?linkelement .

            }}"""

            
            results = linkset.linkset.query(query)
            links = {}

            for item in results:
                link_id = str(item[0]).split('/')[-1]
                linkelement_id = str(item[1]).split('/')[-1]
                if link_id not in links.keys(): links[link_id] = []
                document = None
                identifier = None
                query_linkelement = """
                    PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 
                    PREFIX linkset: <https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

                    SELECT ?document ?identifier
                    WHERE {{
                        OPTIONAL{{<{}> linkset:hasDocument ?document}}.
                        OPTIONAL{{<{}> linkset:hasIdentifier ?identifier}} .
                    }}""".format(str(item[1]), str(item[1]))
                
                linkelement_results = linkset.linkset.query(query_linkelement)
                for linkelement_item in linkelement_results:
                    identifier_type = None

                    document = self.get_document_by_id(str(linkelement_item[0]).split('/')[-1])
                    print(document)
                    
                    query_identifier_type = """
                        PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 
                        PREFIX linkset: <https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

                        SELECT ?value
                        WHERE {{
                            <{}> rdf:type ?value .
                        }}""".format(str(linkelement_item[1]))
                    
                    query_identifier_attributes = """
                        PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 
                        PREFIX linkset: <https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

                        SELECT ?attribute ?value
                        WHERE {{
                            <{}> ?attribute ?value .
                        }}""".format(str(linkelement_item[1]))
                    
                    identifier_type_results = linkset.linkset.query(query_identifier_type)
                    for ids in identifier_type_results:
                        identifier_type = ids[0].fragment
                        
                    if identifier_type == "URIBasedIdentifier":
                        identifier = URIBasedIdentifier(uri = '')

                        identifier_attributes_result = linkset.linkset.query(query_identifier_attributes)
                        for identifier_attr in  identifier_attributes_result:
                            if identifier_attr[0].fragment in identifier.attr_frag_map.keys():
                                identifier.__setattr__(identifier.attr_frag_map[identifier_attr[0].fragment], identifier_attr[1].value)

                    elif identifier_type == "StringBasedIdentifier":
                        identifier = StringBasedIdentifier(identifier ='')

                        identifier_attributes_result = linkset.linkset.query(query_identifier_attributes)
                        for identifier_attr in  identifier_attributes_result:
                            if identifier_attr[0].fragment in identifier.attr_frag_map.keys():
                                identifier.__setattr__(identifier.attr_frag_map[identifier_attr[0].fragment], identifier_attr[1].value)

                    elif identifier_type == "QueryBasedIdentifier":
                        identifier = QueryBasedIdentifier(query_language='', query_exression='')

                        identifier_attributes_result = linkset.linkset.query(query_identifier_attributes)
                        for identifier_attr in  identifier_attributes_result:
                            if identifier_attr[0].fragment in identifier.attr_frag_map.keys():
                                identifier.__setattr__(identifier.attr_frag_map[identifier_attr[0].fragment], identifier_attr[1].value)
                    
                links[link_id].append(LinkElement(id = linkelement_id, document=document, identifier=identifier))
            for link in links.keys():
                linkset.add_link(Link(id=link, a= links[link][0], b = links[link][1]))
            linkset.reset_graph()
            self.add_linkset(linkset)

        # read index graph
        self.index.parse(temp_path + str('index.ttl')) # añadirpara que se pueda en otros formatos rdf (.rdf, .nt ... )

        # read container information
        query = """
            PREFIX container: <https://standards.iso.org/iso/21597/-1/ed-1/en/Container#> 

            SELECT ?attribute ?value
            WHERE {
                ?instance rdf:type container:ContainerDescription .
                ?instance ?attribute ?value .
            }"""
        
        results = self.index.query(query)
        for item in results:
            if item[0].fragment in self.attr_frag_map.keys():
                self.__setattr__(self.attr_frag_map[item[0].fragment], item[1].value)
            else:
                if item[0].fragment == 'containsDocument':
                    get_document(item[1])
        
        for item in results:
            if item[0].fragment == 'containsLinkset':
                get_linkset(item[1])
        
        self.reset_index_graph()


