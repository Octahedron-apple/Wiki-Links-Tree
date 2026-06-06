import re
from pathlib import Path
from pyvis.network import Network

class File_Reader:
    def __init__(self, path):
        self.path = path
        self.md_files = [[str(p), []] for p in Path(self.path).rglob("*.md")]
        # Reads all Files in CWD

    def Read_file(self, file):
        if isinstance(file, int):
            file_index = file
        elif isinstance(file, str):
            try:
                file_index = next(i for i, v in enumerate(self.md_files) if v[0] == file)
            except StopIteration:
                raise ValueError(f"File '{file}' not found in md_files")
        else:
            raise TypeError("file parameter must be an int (index) or str (path)")
        
        with open(self.md_files[file_index][0], 'r') as f:
            a = f.read()
        
        links = re.findall(r'\[\[(.*?)\]\]', a)
        self.md_files[file_index][1] = links

    def Make_Graph(self):
        net = Network(directed=False)
        
        for file_info in self.md_files:
            file_path = file_info[0]
            node_id = Path(file_path).stem
            net.add_node(node_id, label=node_id)
            
        for file_info in self.md_files:
            file_path = file_info[0]
            links = file_info[1]
            source_id = Path(file_path).stem
            
            for link in links:
                target_id = link.split("|")[0].strip()
                if target_id not in net.get_nodes():
                    net.add_node(target_id, label=target_id)
                net.add_edge(source_id, target_id)
                
        net.show('wiki_graph.html', notebook=False)

def main():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    reader = File_Reader(path)
    
    for i in range(len(reader.md_files)):
        reader.Read_file(i)
        
    reader.Make_Graph()
    print("Graph generated as wiki_graph.html")

if __name__ == "__main__":
    main()
