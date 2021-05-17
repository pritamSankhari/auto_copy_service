import sys    
import os

in_filename = sys.argv[1]

# data = open(in_filename, mode="r",encoding="utf8").read()

out_file_basename = os.path.basename(in_filename).split('.')[0]

if len(sys.argv) > 2:
    out_dir = sys.argv[2]
else:
    out_dir = os.path.dirname(os.path.realpath(__file__))

out_filename = os.path.join(out_dir,out_file_basename+'.txt')







with open(in_filename, mode="r",errors="ignore") as f:
    
    data = f.read()

    encoded = data.encode(encoding="utf-8")
    
    # encoded_as_string = str(encoded).strip("b'")
    
    f1 = open(out_filename,"w") 
    for ch in encoded:
        # print(ch)
        f1.write(str(ch))
        f1.write("\n")

    # f.write(encoded_as_string)

    f1.close()
