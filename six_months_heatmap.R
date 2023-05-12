args = commandArgs(trailingOnly=TRUE)

data <- read.table(file=args[1], sep="\t", dec=".", header=TRUE, quote="\"")

rownames(data) <- data[,1]

colnames(data) <- c("Genes", "2WT-6m_S11", "3WT-6m_S1", "5WT-6m_S12", "8WT-6m_S2", "9WT-6m_S3", "10WT-6m_S4", "2AD-6m_S5", "4AD-6m_S7", "5AD-6m_S6", "8AD-6m_S8", "9AD-6m_S9", "10AD-6m_S10")

library(pheatmap)

annotation <- data.frame(sample_group=rep(c("Genes", "WT_6M", "AD_6M"), c(1,6,6)))

row.names(annotation) <- colnames(data)

anno_colors = list ( sample_group= c (WT_6M="green", AD_6M="red"))

pheatmap(log2(data[,2:13]+2), scale="row", show_colnames=FALSE, show_rownames=TRUE, cluster_cols=FALSE, cluster_rows=TRUE, annotation_col=annotation, annotation_colors=anno_colors,
	 main=args[2], cex.main=0.1, height= 10, width=12, annotation_names_col = TRUE, filename=args[3], display_numbers=TRUE)
