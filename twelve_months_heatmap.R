args = commandArgs(trailingOnly=TRUE)

data <- read.table(file=args[1], sep="\t", dec=".", header=TRUE, quote="\"")

rownames(data) <- data[,1]

colnames(data) <- c("Genes", "2WT-12m_S1", "3WT-12m_S1", "5WT-12m_S2", "8WT-12m_S3", "9WT-12m_S4", "10WT-12m_S5", "2AD-12m_S6", "4AD-12m_S2", "5AD-12m_S7", "8AD-12m_S8", "9AD-12m_S9", "10AD-12m_S10")

library(pheatmap)

annotation <- data.frame(sample_group=rep(c("Genes", "WT_12M", "AD_12M"), c(1,6,6)))

row.names(annotation) <- colnames(data)

anno_colors = list ( sample_group= c (WT_12M="green", AD_12M="red"))

pheatmap(log2(data[,2:13]+2), scale="row", show_colnames=FALSE, show_rownames=TRUE, cluster_cols=FALSE, cluster_rows=TRUE, annotation_col=annotation, annotation_colors=anno_colors,
	 main=args[2], cex.main=0.1, height= 10, width=12, annotation_names_col = TRUE, filename=args[3], display_numbers=TRUE)
