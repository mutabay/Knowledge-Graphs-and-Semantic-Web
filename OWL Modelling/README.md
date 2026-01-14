# **OWL Modelling: Web Ontology Language**

## **What is OWL?**
OWL is formal logic for the semantic web. It adds complex relationships and reasoning capabilities to RDF graphs through description logic.

**Core Philosophy**: Express what can be inferred about the world through logical axioms.

## **Basic Class Modeling**

### **Simple Hierarchies (Task 1-4.owx)**
Build taxonomies with inheritance:
```owl
<SubClassOf>
    <Class IRI="#Person"/>
    <Class IRI="#Human"/>
</SubClassOf>
```

**Disjoint Classes:**
```owl
<SubClassOf>
    <Class IRI="#Man"/>
    <Class IRI="#Person"/>
</SubClassOf>
<SubClassOf>
    <Class IRI="#Woman"/>
    <Class IRI="#Person"/>
</SubClassOf>
```

### **Complex Class Definitions**
Define classes through relationships:
```owl
<EquivalentClasses>
    <Class IRI="#Parent"/>
    <ObjectIntersectionOf>
        <Class IRI="#Person"/>
        <ObjectSomeValuesFrom>
            <ObjectProperty IRI="#hasChild"/>
            <Class IRI="#Person"/>
        </ObjectSomeValuesFrom>
    </ObjectIntersectionOf>
</EquivalentClasses>
```
**Meaning**: Parent ≡ Person ⊓ ∃hasChild.Person

## **Property Engineering**

### **Property Hierarchies**
```owl
<SubObjectPropertyOf>
    <ObjectProperty IRI="#hasDaughter"/>
    <ObjectProperty IRI="#hasChild"/>
</SubObjectPropertyOf>
```

### **Inverse Properties**
```owl
<InverseObjectProperties>
    <ObjectProperty IRI="#hasChild"/>
    <ObjectProperty IRI="#isChildOf"/>
</InverseObjectProperties>
```

### **Domain/Range Restrictions**
```owl
<ObjectPropertyDomain>
    <ObjectProperty IRI="#hasChild"/>
    <Class IRI="#Person"/>
</ObjectPropertyDomain>
<ObjectPropertyRange>
    <ObjectProperty IRI="#hasChild"/>
    <Class IRI="#Person"/>
</ObjectPropertyRange>
```

## **Boolean Operations (Task 5.owx)**

### **Complement**
```owl
<EquivalentClasses>
    <Class IRI="#F"/>
    <ObjectComplementOf>
        <Class IRI="#C"/>
    </ObjectComplementOf>
</EquivalentClasses>
```

### **Union**
```owl
<EquivalentClasses>
    <Class IRI="#G"/>
    <ObjectUnionOf>
        <Class IRI="#A"/>
        <Class IRI="#B"/>
    </ObjectUnionOf>
</EquivalentClasses>
```

## **Data Properties and Individuals**

### **Type-Safe Data Binding**
```owl
<DataPropertyAssertion>
    <DataProperty IRI="#hasAge"/>
    <NamedIndividual IRI="#Peter"/>
    <Literal datatypeIRI="xsd:integer">40</Literal>
</DataPropertyAssertion>
```

**Standard XSD Types:**
- name: xsd:string
- hasAge: xsd:integer  
- birthday: xsd:dateTime

### **Individual Classification**
```owl
<ClassAssertion>
    <Class IRI="#Woman"/>
    <NamedIndividual IRI="#Anna"/>
</ClassAssertion>
<ObjectPropertyAssertion>
    <ObjectProperty IRI="#hasChild"/>
    <NamedIndividual IRI="#Peter"/>
    <NamedIndividual IRI="#Lena"/>
</ObjectPropertyAssertion>
```

## **Essential OWL Constructs**

### **Quantifiers**
```owl
<!-- Existential: At least one -->
<ObjectSomeValuesFrom>
    <ObjectProperty IRI="#hasChild"/>
    <Class IRI="#Person"/>
</ObjectSomeValuesFrom>

<!-- Universal: All children -->
<ObjectAllValuesFrom>
    <ObjectProperty IRI="#hasChild"/>
    <Class IRI="#Woman"/>
</ObjectAllValuesFrom>
```

### **Cardinality Constraints**
```owl
<ObjectMinCardinality cardinality="1">
    <ObjectProperty IRI="#hasParent"/>
</ObjectMinCardinality>
<ObjectMaxCardinality cardinality="2">
    <ObjectProperty IRI="#hasParent"/>
</ObjectMaxCardinality>
```

### **Complex Equivalences**
```owl
<EquivalentClasses>
    <Class IRI="#HappyMother"/>
    <ObjectSomeValuesFrom>
        <ObjectProperty IRI="#hasHappyDaughter"/>
        <Class IRI="#HappyMother"/>
    </ObjectSomeValuesFrom>
</EquivalentClasses>
```

## **Reasoning Capabilities**

### **Automatic Inference**
1. **Subsumption**: If Anna is Woman, then Anna is Person
2. **Property chains**: If hasDaughter ⊑ hasChild, constraints propagate
3. **Consistency**: Check logical contradictions
4. **Classification**: Infer class membership

### **Common Reasoning Tasks**
```owl
<!-- Check satisfiability -->
- Can HappyMother have instances?
- Are Man and Woman truly disjoint?

<!-- Property inheritance -->
- Domain/range propagation through subproperties
- Inverse property implications
```

## **Working with OWL Files**

### **Development Tools**
- **Protégé**: Visual ontology editor with reasoning
- **HermiT/Pellet**: Description logic reasoners
- **OWL API**: Programmatic ontology manipulation

### **File Formats**
- **.owx**: OWL/XML functional syntax
- **.owl**: RDF/XML serialization  
- **.ttl**: Turtle with OWL vocabulary

## **Real Applications**
- **Biomedical ontologies**: Disease classification and drug interactions
- **Enterprise knowledge**: Business process modeling and rules
- **Data integration**: Schema mapping and transformation
- **Question answering**: Semantic search and inference

OWL transforms simple RDF graphs into powerful knowledge bases through formal logic and automated reasoning.
