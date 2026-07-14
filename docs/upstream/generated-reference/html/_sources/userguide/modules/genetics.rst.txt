.. _userguide-modules-genetics:genetics:

Genetics
========

.. _userguide-modules-genetics:genetics-overview:

Overview
--------

GNU Health medical genetics functionality is provided by the following packages:

* health_genetics
* health_genetics_uniprot

GNU Health genetic functionality combines the molecular and environmental bases
of health and disease unique for each individual, foundation for precision medicine.

The GNU Health genetic functionality can be used both in the clinical and
research contexts.

GNU Health incorporates extensive information from **Hugo Gene Nomenclature Committee**
(HGNC) **The National Center for Biotechnology Information** :wikipedia:`NCBI`
and from **the** :wikipedia:`UniProt` **Consortium** gene natural variants
and protein-related human health conditions.

The screenshots provided on this section aim to facilitate the usage
of the genetic packages, as basic workflows and data entry. We will be using
two of our (fictional) family members Ana Betz and her son, Matt.
The CFTR (Cystic Fibrosis transmembrane conductance regulator) will be used
to illustrate different objects and contexts of the GH genetic functionality.



.. _userguide-modules-genetics:genetics-core_genetics_package:

Core genetics package
---------------------

GNU Health genetic related packages integrate family history
and individual relevant genetic information.

The core genetics package provides main functionality, datamodel and
relationships with other objects in the GNUHealth data dictionary.

The main models included in this package are:

* Genes
* Protein related diseases
* Family History
* Personal genetic information
* Natural variants
* Variants phenotypes.

The Genes model which its atributes will be detailed next wil hold the
HGCN dataset, which is also included on the health_genetics package.

**The Gene Model**

The main attributes are:

* **HGNC Id**: HUGO Gene Nomenclature Committee ID for the gene.
* **Official Symbol**: Gene symbol dictated by HGNC (eg .. CFTR)
* **Long Name**: Official long name (eg CF transmembrane conductance regulator)
* **Aliases**: Alternative symbols (eg .. MRP7|ABC35|TNR-CFTR|dJ760C5.1|CFTR/MRP)
* **Locus**: Location of the gene in the chromosome
* **Type**: Type of gene (eg, protein-coding, ncRNA, pseudogene..)
* **Variants**: List of natural variants associated to the gene (from UniProt)
* **Encoding protein** (ID and URI)

There are other fields such as RefSeq, Ensembl and OMIM IDs that help
referencing related resources.


**Natural Variant**

* Gene
* Change in amino acid
* Phenotype
* Clinical significance

  * LB/B: Likely benign or benign
  * LP/P: Likely pathogenic or pathogenic
  * US: Unknown Significance

**Variant Phenotype(s)**


.. _userguide-modules-genetics:genetics-core_genetics_package-accessing_the_genes_dataset:

Accessing the genes dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can access the genes dataset via menu or via GH Command line.

**Menu**: Health -> Configuration -> Genetics -> Genes

**Command Line** : gdis

.. thumbnail:: ../../images/gnuhealth_genetics_genes_list_view.png
    :title: Genes list view.



.. _userguide-modules-genetics:genetics-core_genetics_package-filtering_/_refining_the_search_criteria:

Filtering / refining the search criteria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As in any model in GNU Health, you can restrict the search combining
search arguments.

.. thumbnail:: ../../images/gnuhealth_genetics_gene_filter_options.png
    :title: Select protein-coding genes with the symbol containing the
            substring "CFTR" from the general list.


.. _userguide-modules-genetics:genetics-core_genetics_package-viewing_details_of_the_gene:

Viewing details of the gene
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have selected the gene in particular from the list view, you
can access the form / detailed view by double clicking on it.
In our example of the CFTR gene:

.. thumbnail:: ../../images/gnuhealth_genetics_gene_cftr_detailed_view.png
    :title: Form view showing the detailed information of the CFTR gene.
            The tooltip from the globe icon shows the URL from UniProt
            of the related protein product ID (P13569) of the gene.



.. _modulesindetail-genetics:genetics-genetic_information:


.. _userguide-modules-genetics:genetics-health_genetics_uniprot_package:

Health Genetics UniProt Package
-------------------------------

While the genetics core package defines the genomics and medical genetics
models, the health_genetics_uniprot loads the meaningful data.

The datasets included in this package are:

* Human genes natural variants
* Variant phenotypes
* Genetic and Protein Related Disorders


.. _userguide-modules-genetics:genetics-health_genetics_uniprot_package-human_genes_natural_variants:

Human Genes Natural Variants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GNU Health HIS combines HGNC with the UniProt human natural variants
datasets. These two excellent sources provide acurate information
and links to uptodate online references to the particular variant related to
the patient.

Previously we saw that when selecting a particular gene we can see the all its
natural variants. In the tree view, you will see a number. In the CFTR gene,
the shows that contains 191 natural variants.


.. _userguide-modules-genetics:genetics-health_genetics_uniprot_package-variant_phenotypes:

Variant Phenotypes
^^^^^^^^^^^^^^^^^^

GNU Health also provides a way to study the phenotypes associated to
the gene natural variants. We can access the variant phenotypes via
command line or menu:


* Command line: **"VARP"**
* **Menu** : Health -> Configuration -> Genetics -> Variant Phenotypes

We can search for a particular phenotype or disorder, a change in the
aminoacid, the gene or the feature ID of the variant (FTid).

In our example of the CFTR gene, we highlight the fact of a particular
variant responsible of more than one phenotype. In the example, variant
with UniProt FTid VAR_000119 (aa change p.Asp110His) has been documented
to be involved in two phenotypes:

- DI-01389: Congenital bilateral absence of the vas deferens
- DI-01466: Cystic fibrosis


.. thumbnail:: ../../images/gnuhealth_genetics_variants_phenotypes_cftr.png
    :title: Example of involvement of a particular variant in two
            different phenotypes.


.. _userguide-modules-genetics:genetics-health_genetics_uniprot_package-genetic_and_protein_related_disorders:

Genetic and Protein Related Disorders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The GNU Health genetics **UniProt** package provides over 6400 genetic and
protein related disorders.

.. thumbnail:: ../../images/gnuhealth_genetics_genetic_and_protein_diseases.png
    :title: List view of genetic diseases, with the Barth Syndrome entry
            selected (highlighted)

There are several ways to access or group the disorders.

* **Disease ID**: Uniprot provided unique ID per disorder, with the format DI-XXXXX
* **Disease Name**: Long, descriptive name of the disorder
* **Mnemonic**: Simpler, one word that identifies the disorder
* **Xrefs**: Cross references for well known database (OMIM, MedGen, MeSH...)
* **Keywords**: Handy way to search disorders by groups (eg, cardiomyopathies, neurodegeneration,...)
* **Inheritance pattern**: The mode of passing the disorder to offsprings (eg, autosomal dominant/recessive, X-Linked..)


In addition to the fields shown in the previous screenshot corresponding to
the list view, the form view provides the disease URI (pointing to UniProt
disease entry online resource), a detailed description of the disorder,
the gene(s) involved, the protein product and the list of natural variants
related to the disorder.


.. thumbnail:: ../../images/gnuhealth_genetics_genetic_and_protein_diseases_form_view.png
    :title: Detailed (form) view for the Barth Syndrome disease entry (DI-0005).



.. _modulesindetail-genetics:genetics-protein_related_diseases-natural_variants:


.. _userguide-modules-genetics:genetics-personal_genetic_information:

Personal Genetic Information
----------------------------

GNU Health stores the details on each of the genes that are relevant for
the individual. This information can be accessed from the "Genetics" tab
on the patient main form.

* **Gene involved**: Information about the gene. The gene code, official
  long name, chromosome and locus. It also provides information about the
  protein encoded and the link to UniProt protein code.

* **Natural Variant**: The specific amino acid change.

* **Phenotype**: This field is used if the person shows clinical
  signs associated to the expression of that gene variant.

* **Onset** : Age (expressed in years) of first clinical signs.

* **Notes** : Comments contextualized to the individual.

If we rather want to see the genetic information at population level,
then we can use the menu:


**Health -> Personal Genetic Information**

.. _userguide-modules-genetics:genetics-family_history:

Family History
--------------

GNU Health shows extra info related to diseases including the name,
code and main disease category, genetic data and a free text box for
adding relevant extra info.

.. _modulesindetail-genetics:genetics-protein_related_diseases:

.. thumbnail:: ../../images/gnuhealth_genetics_ana_betz_family_history.png
    :title: The family history is encoded on the right hand side section
            of the patient genetics tab.


.. _userguide-modules-genetics:genetics-genetic_testing_and_medical_history:

Genetic testing and Medical history
-----------------------------------

So far we've seen how to register the genetic information and family
history of the individual, and we know will see how to register a
particular phenotype or disorder.

A positive result of a particular genetic test does not necessarily equates
to disease, as we see in many late-onset disorders.

In our family example, Ana Betz is a (healthy) carrier for a pathogenic
variant in the CFTR gene, involved in cystic fibrosis.

Her son, Matt, carries two pathogenic alleles of the CFTR and he shows
clinical signs compatible with Cystic Fibrosis.

When both the molecular testing and the clinical signs are present, we can
then encode the corresponding ICD11 (or whatever coding standard)
corresponding with the disease.



Ana Betz has a child (Matt). Cystic fibrosis is has a autosomal recessive
inheritance pattern, that is, two pathogenic alleles are required to
develop different signs of cystic fibrosis.

Matt has inherited two dysfunctional alleles, one from the mother (var_000179) and
one from the father (var_000267). Because both alleles have been identified by
molecular testing, **and** he has shown clinical signs compatible with the
cystic fibrosis, the corresponding ICD11 (CA25) has been incorporated to
his medical history.

.. thumbnail:: ../../images/gnuhealth_genetics_variants_phenotypes_patient_information_matt.png
    :title: Some of the elements related to the molecular diagnostics and
            medical history of a particular individual.



.. _userguide-modules-genetics:genetics-gnu_health_commands_for_genetics:

GNU Health Commands for genetics
--------------------------------

* **gen**: Personal Genetic Information

* **gdis**: Genes

* **var**: Natural Variants

* **varp**: Variant Phenotypes

* **pdis**: Genetic / Protein diseases

The GNU Health commands allow arguments. For example, if you want to get
the information related to the CFTR gene, you can type in the command
line widget:

.. code-block::

    gdis CFTR


To retrieve a CFTR natural variant its Feature ID (FTid) var_000179

.. code-block::

    var VAR_000179



If you want to see the genetic information for a particular patient:

.. code-block::

    gen GNU777ORG



To access the latest information about cystic fibrosis:

.. code-block::

    pdis DI-01466


.. thumbnail:: ../../images/gnuhealth_genetics_gen_command.png
    :title: gen command to retrieve the personal genetic information for the
            ID "GNU777ORG" (Ana Betz)


