# VOC

The XML-based annotation format was introduced by the 
[PASCAL Visual Object Classes](http://host.robots.ox.ac.uk/pascal/VOC/).

Here is an example:

```xml
<annotation>
	<folder></folder>
	<filename>image_0001.jpg</filename>
	<path>image_0001.jpg</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>689</width>
		<height>500</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>Daffodil</name>
		<pose>0</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<occluded>0</occluded>
		<bndbox>
			<xmin>86</xmin>
			<xmax>583</xmax>
			<ymin>80</ymin>
			<ymax>388</ymax>
		</bndbox>
	</object>
</annotation>
```
