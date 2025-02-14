library(igraph)

n <- 100
ring <- make_ring(n)
p <- 1:10 / 10 
print(p)
print(summary(ring))
hc <- harmonic_centrality(ring)
cat(1:100, sep='\t', file="ps2_q6.tsv")
cat("\n", file="ps2_q6.tsv", append=TRUE)
cat(hc, sep='\t', file="ps2_q6.tsv", append=TRUE)

G_cf <- ring
for (p_i in p) {
    G_cf <- rewire(G_cf, with = each_edge(p_i))
    hc_cf <- harmonic_centrality(G_cf)
    cat(hc_cf, sep='\t', file="ps2_q6.tsv", append=TRUE)
    cat("\n", file="ps2_q6.tsv", append=TRUE)
}

