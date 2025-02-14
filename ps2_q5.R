library(igraph)
library(tidyverse)
g <- read_graph("medici_network.gml", format = "gml")
print(summary(g))
nme <- vertex_attr(g, "label")
hc <- harmonic_centrality(g)
m <- gsize(g)
# write.table(data.frame(nme, hc), "ps2_q5_hc.tsv", sep = "\t", row.names = FALSE, quote = FALSE)

# cat(c("r", nme), sep='\t', file="ps2_q5b.tsv")
# cat("\n", file="ps2_q5b.tsv", append=TRUE)
# cat(c("0", hc), sep='\t', file="ps2_q5b.tsv", append=TRUE)
# cat("\n", file="ps2_q5b.tsv", append=TRUE)

# # do config model and compute hc
# # first config model
# r_cf1 <- 20 * m
# G_cf1 <- rewire(g, keeping_degseq(niter=r_cf1))
# hc <- harmonic_centrality(G_cf1)
# cat(c(r_cf1, hc), sep='\t', file="ps2_q5b.tsv", append=TRUE)
# # next 1000 config models
# r_cf <- r_cf1
# G_cfi <- G_cf1
# for (i in 1:999) {
#     G_cfi <- rewire(G_cfi, keeping_degseq(niter=2 * m))
#     r_cf <- r_cf + (2 * m)
#     cat(c(r_cf, harmonic_centrality(G_cfi)), sep='\t', file="ps2_q5b.tsv", append=TRUE)
#     cat("\n", file="ps2_q5b.tsv", append=TRUE)
# }


# plot
data <- read_tsv("ps2_q5b.tsv")
# rm row 1
data <- data[-1,]
print(data)
# deselect col1
data <- data[,-1]
print(data)
# find which values are not numeric
for (i in 1:ncol(data)) {
    data[[i]] <- as.numeric(data[[i]])
}
# flatten and do hist
flat <- as.vector(as.matrix(data))
colors <- c("red", "blue", "green", "purple", "orange", "brown", "pink", "cyan", "magenta", "yellow", "gray", "black", "darkgreen", "darkblue", "darkred", "gold")
png("ps2_q5b.png", width = 1000, height = 600)
par(mfrow=c(1,2))
hist(flat, breaks=100, col="lightblue", xlab="Node harmonic centrality", main="Harmonic centrality of nodes from 1000 configuration models", ylab="Count", cex.axis=1.2, cex.lab=1.5)
for (i in 1:length(hc)) {
    # do vline
    abline(v=hc[i], col=colors[i], lwd=2)
}
plot.new()
legend("center", legend = nme, col = colors, lwd = 2, cex = 1.2, bty = "n")
dev.off()

