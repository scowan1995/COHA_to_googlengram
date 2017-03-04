import nose
import convert


class ConversionTest():

    def __init__(self):
        self.path = "/Users/Sean/FYP/CodeForSean\
        /convert/news_1942_706831.txt"
        self.file_of_files = "/Users/Sean/FYP/CodeForSean/convert/fs.txt"

    def test_get_paths(self):
        assert (convert.get_paths(self.file_of_files) == self.path)

    def test_build_name(self):
        assert (convert.build_name(self.path) == "news_706831_1942")
