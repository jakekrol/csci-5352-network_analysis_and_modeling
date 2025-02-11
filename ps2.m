% Load edge list from file
edgeList = readmatrix('Berkeley13.txt'); % Assumes file contains [src, dest, weight]

% Extract source, destination, and weights
src = edgeList(:, 1);
dest = edgeList(:, 2);

% Create a graph (use 'graph' for undirected, 'digraph' for directed)
G = digraph(src, dest); % Use 'graph' if the graph is undirected

% % Compute All-Pairs Shortest Paths (APSP)
% APSP = distances(G);
% 
% % Display the shortest path distance matrix
% % disp(APSP);
% 
% N = size(APSP, 1); % Number of nodes
% APSP_noInf = APSP(~isinf(APSP)); % Ignore unreachable nodes (Inf values)
% 
% % Compute the mean of all finite distances
% avgPathLength = mean(APSP_noInf);
% 
% % Display result
% fprintf('Average Path Length: %.4f\n', avgPathLength);

function G = doubleEdgeSwap(G, numSwaps)
    % DOUBLEEDGESWAP Performs double-edge swaps on a graph G
    % numSwaps: Number of swaps to perform
    
    % Extract edge list
    [src, dest] = find(tril(adjacency(G)));  % Get edges (for undirected graph)
    edges = [src, dest];  % Store edges in a matrix
    numEdges = size(edges, 1);
    
    for i = 1:numSwaps
        % Randomly pick two distinct edges
        idx = randperm(numEdges, 2);
        e1 = edges(idx(1), :);
        e2 = edges(idx(2), :);
        
        % Extract endpoints
        u = e1(1); v = e1(2);
        x = e2(1); y = e2(2);
        
        % Ensure the new edges do not already exist and avoid self-loops
        if length(unique([u, v, x, y])) == 4 && ...
           ~ismember([u, y], edges, 'rows') && ...
           ~ismember([x, v], edges, 'rows')
       
            % Perform the swap
            edges(idx(1), :) = [u, y];
            edges(idx(2), :) = [x, v];
        end
    end
    
    % Create new graph with swapped edges
    G = graph(edges(:,1), edges(:,2));
end
