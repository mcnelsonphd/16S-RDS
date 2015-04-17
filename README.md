#Introduction
This is the official project home for the scripts necessary to carry out the various pre-processing and analysis steps that are recommended and implemented in the RDS processing scheme published by __[Nelson et al., PLoS ONE 9: e94249. doi:10.1371/journal.pone.0094249](http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0094249 "Nelson et al., Analysis, Optimization and Verification of Illumina-Generated 16S Amplicon Surveys, PLoS ONE (2014) 9:e94249").__

The primary scripts for carrying out the full processing and anlaysis pipeline are __V4-Preprocess__ and __Qiime\_Analysis__, however the user must perform split_libraries_fastq.py themselves.

###1. V4-Preprocess
__V4-Preprocess__ is the first step of the analysis pipeline. It takes the three raw Undetermined files from the MiSeq and proceeds with read-merging using SeqPrep, phiX identification via bowtie2 and removal, and length filtering of reads that fall outside the expected size range for V4 amplicons (< 240, > 265 bp) using a custom biopython script. The final results of this step are a Good\_Reads\_filtered\_DATE-TIME.fastq.gz and Good\_Index\_filtered\_DATE-TIME.fastq.gz file. Intermediate files are placed in a V4\_Intermediates\_DATE-TIME directory. The script operates on a checkpointing scheme and will attempt to restart after the last successfully completed step in case of failure.

__Useage:__ 
```shell
cd /Directory_containing_raw_read_files
V4_Preprocess
```
__Note:__ The gzip compression used by MiSeq Reporter is somehow different than the gzip native to OSX and possibly linux. MD5 checksum values are calculated of the original Undetermined files, as well as after completion of the pre-processing steps. These values will likely differ due to the aformentioned compression differences. To compensate, the MD5 values of the uncompressed files are also calculated as these values should not change regardless of the compression system used.

###2. Qiime\_Processs
__Qiime_Process__ is the second step of the analysis pipeline and will take demultiplexed sequences and proceed through a pre-defined set of QIIME analyses, principally involving reference OTU assignment followed by *de novo* OTU assignment of reads that failed to be assigned to a reference OTU as recommended and implemented in the RDS processing method. The user supplies the script with their QIIME demultiplexed sequences in FASTA format, the sample mapping file, and optionally their desired rarefaction depth and the script will proceed through OTU assignment, chimera checking with ChimeraSlayer, OTU table filtering, taxonomy assignment, and simple alpha and beta diversity analyses of both un-normalized and normalized data. 

Notes: 
1. The input sequence file can be named anything the user chooses, such as combined_run_seqs.fasta. 
2. If meta-data is included in the sample mapping file, it will be added to the biom formatted OTU tables. 

__Useage:__
```shell
Print help: Qiime_Process -h
Basic:      Qiime_Process -s seqs.fna -m map.txt
Advanced:   Qiime_Process -s spit_libs/seqs.fna -m map_with_metadata.txt -d 5000

```

###3. Reanalyze\_16S
__Reanalyze\_16S__ is an accessory script that may or may not be necessary for users to run. If the results of the Qiime\_Analysis script result in normalization of the samples to a value too small for the users liking, or if they wish to re-run the normalization and resulting alpha and beta diversity analyses using a different number of sequences then this script will allow them to carry this out. To reanalyze using a new number of sequences for normalization, the user needs to supply the script the path to the filtered OTU table, sample mapping file, phylogenetic tree, and the value to be used for rarefaction. The output files will be placed in a subdirectory that is dated and also includes the new rarefaction value passed to the script.

__Useage:__
```shell
Print help: Reanalyze_16S -h
Standard:   Reanalyze_16S -o otu_table.biom -m map.txt -t Rep_Set_tree.tree -d 10000
```

##Accessory Files
- __GreenGenes_References:__ contains V4, V4V5, and V1-V3 reference datasets as gzipped tar archives. Within each archive is an un-aligned and aligned set of reference sequences as well as the taxonomy reference down to the species level.
- __Test_Data:__ contains a very small set of raw sequences for use in testing the implementation of the V4_Preprocess script.
- __phiX:__ contains the phiX index needed by bowtie as part of the V4_Preprocess script.
- __Length_Filter.py:__ is a script utilizing Biopython to size filter sequences as part of V4_Preprocess.

