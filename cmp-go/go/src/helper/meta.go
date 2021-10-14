package helper

import (
	"goml/logger"
	"strconv"
)

type MetaData struct {
	stream interface{}
	data   map[string]float32
	path   string
	reader *CSVReader
}

func (d *MetaData) Load() error {
	if d.reader == nil {
		d.reader = &CSVReader{}
	}

	if d.data == nil {
		d.data = make(map[string]float32)
	}

	// return d.reader.Load(d.path)

	log := logger.GetLogger("MetaData")
	if err := d.reader.Load(d.path); err != nil {
		return err
	}

	for _, row := range d.reader.GetData() {
		v, _ := strconv.ParseFloat(row[1], 32)
		d.data[row[0]] = float32(v)
	}

	log.Debug("%v", d.data)
	return nil
}

func (d *MetaData) SetFile(path string) {
	d.path = path
}

func (d *MetaData) GetPath() string {
	return d.path
}

func (d *MetaData) Mean() float32 {
	return d.data["mean"]
}

func (d *MetaData) Std() float32 {
	return d.data["std"]
}

func (d *MetaData) ToArray() [][][]float32 {
	return nil
}

func (d *MetaData) SetStream(stream interface{}) {
}

func (d *MetaData) Exist() bool {
	return d.reader.Exist()
}
