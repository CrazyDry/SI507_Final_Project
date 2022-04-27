import regex as re
import json

f = open("IMDB_movie_details.json", "r")
a = f.read()
f.close()

a = a.replace("}\n{", "},{")
a = "[" + a + "]"
b = json.loads(a)

print("# of movie: ", len(b))
# 1572

new = {}
for item in b:
    new[item['movie_id']] = item

output_json = open("IMDB_movie_info.json", "w")
contents_to_write = json.dumps(new, indent=2)
output_json.write(contents_to_write)
output_json.close()