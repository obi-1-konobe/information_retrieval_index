from my_parser import Parser
import configs as c
from preprocess_document import Preprocessor

# p = Parser()
# p.run(c.STOP_DOWNLOAD_SIZE)

pp = Preprocessor()
asd = pp.get_terms('corpus/482818.txt')
print(asd)