
---
title: 0501-poplar
mustache: ./vars.yaml

bibliography: ./citation.bib
csl: science.csl
include-in-header:
	- \usepackage{times}
---

## Computational analysis:

1. <u>DAP-Seq: Mapping, quantification and peak calling</u>
	
	* Adapters were trimmed off from raw reads with "trim_galore" (!CITE!TRIM_GALORE). Raw reads were mapped to the genome {{GENOME}} with Bowtie2 (@BOWTIE2) under argument:\"{{ARG_BOWTIE2}}\". Duplicate reads were removed with Picard using default setting (!CITE!PICARD). The resultant alignment is used for downstream quantification and visualisation

	* Genomic binding profile was quantified in RPKM (Reads Per Kilobase per Million mapped reads) using a bin-size of {{BIN_CHIP}}bp. For each bin, $\text{RPKM}_{\text{bin}}=\frac{\# \text{Reads covering bin}} { \text{bin-size} } \cdot \frac{10^6}{ \#\text{Mapped reads}}$

	* For each treated DAP-Seq library, peaks were called against a control library using MACS2 (!CITE!MACS2) with argument \"{{ARG_MACS2}}\". Peaks from each DAP-Seq were further fitlered for {{MACS2_FILTER}}.
    
    * Any gene with a peak within +/- {{CUTOFF_PEAK2GENE}} of its start codon is considered a target gene. Best arabidopsis homologue is reported for each target gene, using annotation file {{ANNO_INFO}}. 

1. <u>Availability and external packages</u>

	* Post-processing code is available as tarball as attached in the supplementary. It depends on python2 packages [pymisca](https://github.com/shouldsee/pymisca) and [synotil](https://github.com/shouldsee/synotil).

	* DAP-Seq data are available from: {{GEO_CHIP}}

	* GNU-parallel (!CITE!GNUPARA) was used in paralleling the computational analysis. 
    
    * Bedtools (!CITE!BEDTOOLS) was used for intersection of peaks, making genomic windows.
    