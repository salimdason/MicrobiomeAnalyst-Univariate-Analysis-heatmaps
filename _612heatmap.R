args = commandArgs(trailingOnly=TRUE)

data <- read.table(file=args[1], sep="\t", dec=".", header=TRUE, quote="\"")

rownames(data) <- data[,1]

colnames(data) <- c("Genes", "2AD-6m_S5", "4AD-6m_S7", "5AD-6m_S6", "8AD-6m_S8", "9AD-6m_S9", "10AD-6m_S10", "2AD-12m_S7", "5AD-12m_S8", "6AD-12m_S9", "8AD-12m_S10", "9AD-12m_S11", "10AD-12m_S12")


library(pheatmap)

annotation <- data.frame(sample_group=rep(c("Genes", "AD_6M", "AD_12M"), c(1,6,6)))

row.names(annotation) <- colnames(data)

anno_colors = list ( sample_group= c (AD_6M="green", AD_12M="red"))

pheatmap(log2(data[,2:13]+2), scale="row", show_colnames=FALSE, show_rownames=TRUE, cluster_cols=FALSE, cluster_rows=TRUE, annotation_col=annotation, annotation_colors=anno_colors,
	 main=args[2], cex.main=0.1, height= 10, width=12, annotation_names_col = TRUE, filename=args[3], display_numbers=TRUE)
