= A web crawler to scrape attendance details

== Some of the xpath to scrape the site

```python
items = response.xpath('//td[@bgcolor="#9f0000"]/font/text()')
datedata = response.xpath('//td[@bgcolor="#aaaaaa"][@height="35"]')

for dates in datedata:
    # leave = dates.xpath('.//following-sibling::td[@bgcolor="#9f0000"]/font/text()')
    date = dates.xpath('.//text()').get()
    abslist = list()
    for i in range(1, 8):
        leaveNo = dates.xpath(f'.//following-sibling::td[{i}]')
        # print(leaveNo.get())
        if leaveNo.attrib["bgcolor"] == "#9f0000":
            abslist.append(leaveNo.xpath('.//text()').get())

```
