#!/bin/python3
import os
import json
from bs4 import BeautifulSoup as bs

flagDir = "./flags"
baseDir = "./base"
outDir = "./out"

for _, _, basefiles in os.walk(baseDir):
	for basef in basefiles:

		for _, _, flagfiles in os.walk(flagDir):
			for flagf in flagfiles:
				with open(os.path.join(baseDir, basef)) as f:
					base = bs(f.read(), "xml")
				with open(os.path.join(flagDir, flagf)) as f:
					flag = json.loads(f.read())["colors"]
				
				for flagpattern in base.find_all(attrs={"data-pride": "1"}):

					startX = float(flagpattern["data-pride-x"])
					startY = float(flagpattern["data-pride-y"])
					directionX = float(flagpattern["data-pride-dx"])
					directionY = float(flagpattern["data-pride-dy"])
					width = float(flagpattern["data-pride-width"])

					totalColorWeight = 0
					for c in flag:
						totalColorWeight = totalColorWeight+c["weight"]
					currentColorWeight = 0
					for c in flag:
						offset = currentColorWeight/totalColorWeight
						#size = c["weight"]/totalColorWeight
						size = currentColorWeight/totalColorWeight

						pA0X = startX+offset*directionX
						pA0Y = startY+offset*directionY

						pAAX = pA0X+width*-directionY
						pAAY = pA0Y+width*directionX

						pABX = pA0X+width*directionY
						pABY = pA0Y+width*-directionX

						pBAX = pAAX+(1-size)*directionX
						pBAY = pAAY+(1-size)*directionY

						pBBX = pABX+(1-size)*directionX
						pBBY = pABY+(1-size)*directionY

						ctag = base.new_tag("path", fill=c["color"], d="M "+str(pAAX)+" "+str(pAAY)+" L "+str(pABX)+" "+str(pABY)+" L "+str(pBBX)+" "+str(pBBY)+" L "+str(pBAX)+" "+str(pBAY))
						flagpattern.append(ctag)
						currentColorWeight = currentColorWeight+c["weight"]

				name = str.replace(basef, "flagname", str.replace(flagf, ".json", ""))
				with open(os.path.join(outDir, name), "w") as f:
					f.write(base.prettify())
