import pytest
from pathlib import Path
from wikilinksgraph.main import File_Reader

def test_file_reader_initialization(tmp_path):
    (tmp_path / "Home.md").write_text("[[Page 1]]")
    (tmp_path / "Page 1.md").write_text("[[Home]]")
    (tmp_path / "ignore.txt").write_text("This should not be parsed.")
    
    reader = File_Reader(str(tmp_path))
    
    assert len(reader.md_files) == 2
    for file_info in reader.md_files:
        assert isinstance(file_info[0], str)
        assert file_info[0].endswith(".md")
        assert isinstance(file_info[1], list)
        assert len(file_info[1]) == 0

def test_read_file_extracts_links(tmp_path):
    home_file = tmp_path / "Home.md"
    home_file.write_text("Here is a link to [[Page 1]] and an aliased link to [[Page 2|alias]].")
    
    reader = File_Reader(str(tmp_path))
    reader.Read_file(str(home_file))
    
    home_idx = next(i for i, f in enumerate(reader.md_files) if f[0] == str(home_file))
    links = reader.md_files[home_idx][1]
    
    assert len(links) == 2
    assert "Page 1" in links
    assert "Page 2|alias" in links

def test_read_file_invalid_input(tmp_path):
    reader = File_Reader(str(tmp_path))
    
    with pytest.raises(ValueError):
        reader.Read_file("non_existent_file.md")
        
    with pytest.raises(TypeError):
        reader.Read_file(3.14)
