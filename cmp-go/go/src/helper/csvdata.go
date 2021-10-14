package helper

type CSVData struct {
	path   string
	reader *CSVReader
}

func (d *CSVData) Load() error {
	if d.reader == nil {
		d.reader = &CSVReader{}
	}
	return d.reader.Load(d.path)
}

func (d *CSVData) SetFile(path string) {
	d.path = path
}

func (d *CSVData) GetPath() string {
	return d.path
}

func (d *CSVData) ToArray() [][][]float32 {
	return csvToArray(d.reader.GetData())
}

func (d *CSVData) SetStream(stream interface{}) {
}

func (d *CSVData) Mean() float32 {
	return 0
}

func (d *CSVData) Std() float32 {
	return 0
}

func (d *CSVData) Exist() bool {
	return d.reader.Exist()
}
