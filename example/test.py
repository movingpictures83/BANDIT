import os

def test(file1, file2):
   firstfile = open(file1, 'r')
   secondfile = open(file2, 'r')
   l1 = firstfile.readline()
   l2 = secondfile.readline()
   if (l1 == l2):
       return True
   else:
       return False
   #lines1 = []
   #lines2 = []
   #for line in firstfile:
   #   lines1.append(line)
   #for line in secondfile:
   #   lines2.append(line)

   #if len(lines1) != len(lines2):
   #   return False

   #for i in range(0, len(lines1)):
   #   indx1 = lines1[i].find("<div id=\"header_filename\">")
   #   if (indx1 != -1):
   #      indx1_F = lines1[i].find("<br", indx1)
   #      indx2 = lines2[i].find("<div id=\"header_filename\">")
   #      indx2_F = lines2[i].find("<br", indx2)
   #      lines1[i] = lines1[i][:indx1] + lines1[i][indx1_F:]
   #      lines2[i] = lines2[i][:indx2] + lines2[i][indx2_F:]
   #   if (lines1[i] != lines2[i]):
   #         return False

   #return True    
