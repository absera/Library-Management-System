# these functions are used in the main app

# this function is used to add the book id
# that is generated above to the main book
# information
def addIdsToMatchedBooks(matched_books, ids):
	finalData = []
	for i, j in zip(matched_books, ids):
		i = list(i)
		i.append(j)
		finalData.append(tuple(i))

	return finalData


# this functions is used to generate new id for the
# accordion
def generateID(id_number):
            alphabet = "abcdefghijk"
            new_id = ""
            for i in str(id_number):
                new_id += alphabet[int(i)]

            return new_id
