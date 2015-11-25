import urllib, urllib2
from bs4 import BeautifulSoup
from lxml import etree 
class WikiSpider():

	def __init__(self):
		self.year = input("Enter Year:-> ")
		self.startUrl = "https://en.wikipedia.org/wiki/%s"%(self.year)
		self.callMethods()


	def callMethods(self):
		self.declareXpath()
		self.openUrl()
		self.getCountries()
		self.parseMainData()

	def declareXpath(self):
		self.countriesXpath = "//td[text()='By country']/../following-sibling::tr[1]//a/@href"
		self.mainHeadingXpath = 	"//span[@class='mw-headline']"
		self.subHeadingXpath = 	"//span[@class='mw-headline']/text()"

	def openUrl(self):
		print "Opening Url :->",self.startUrl		
		url = self.startUrl
		fp = urllib2.urlopen(url)
		self.html = etree.parse(fp)


	def getCountries(self):
		allCountries = []
		counter = 1
		countryDict = {}
		for countryName in self.html.xpath(self.countriesXpath):
			allCountries.append(countryName)
			countryDict[counter] = countryName
			counter = counter + 1
		print "***********************************"
		for data in countryDict:
			print data,":",countryDict[data]
		print "***********************************"
		selectedCountryId = input("Enter Country Id:")
		selectedUrl = countryDict[selectedCountryId]
		print "************************************"
		print "Selected Url : ",selectedUrl
		print "************************************"
		self.selectedUrl = "https://en.wikipedia.org%s"%(selectedUrl)
		print self.selectedUrl
		self.startUrl = self.selectedUrl
		self.openUrl()

	def filterString(self,stringf):
		stringf = str(stringf.encode('ascii', 'ignore'))
		stringf = stringf.replace(',',' ')
		return stringf
		
	def parseMainData(self):
		fileName = "%s-WikiScrapper.csv"%(self.year)
		first_file = open(fileName,'w')
		first_file.write('url')
		first_file.write(',')
		first_file.write('information')
		first_file.write(',')
		first_file.write('subHeading')
		first_file.write('\n')
		for mainContent in self.html.xpath(self.subHeadingXpath):
			headingName = str(mainContent)
			print headingName
			inLoopXpath = "//span[@class='mw-headline' and text()='%s']/../following-sibling::ul[1]/li"%(headingName)
			makeStringsubHeading = ""
			for subContent  in self.html.xpath(inLoopXpath):
				listOfData = subContent.xpath("a/text()")
				# print type(listOfData)
				for cc in listOfData:
					makeStringsubHeading = "%s %s"%(makeStringsubHeading,self.filterString(cc))
				print makeStringsubHeading
				first_file.write(str(self.startUrl))
				first_file.write(',')
				first_file.write(self.filterString(makeStringsubHeading))
				first_file.write(',')
				first_file.write(self.filterString(headingName))
				first_file.write('\n')
				makeStringsubHeading = ''

			print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
		first_file.close()



if __name__ == '__main__':
	obj = WikiSpider()