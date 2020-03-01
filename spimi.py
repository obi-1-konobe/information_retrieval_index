class Index:
    def __init__(self):
        pass

    @staticmethod
    def update_index(index, term_stream, doc_id):
        for term in term_stream:
            if term not in index:
                index[term] = [doc_id]
            else:
                index[term].append(doc_id)


