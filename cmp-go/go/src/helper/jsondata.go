package helper

import (
	"goml/util"
)

type JSONData struct {
	stream interface{}
	data   [][][]float32
}

func (d *JSONData) Load() error {
	arr := util.InterfaceToArray(d.stream)
	arr2D := util.ToArray2D(arr)
	d.data = util.ToArray3D(arr2D)
	return nil
}

func (d *JSONData) SetFile(path string) {
}

func (d *JSONData) GetPath() string {
	return "Use JSON Data stream."
}

func (d *JSONData) ToArray() [][][]float32 {
	return d.data
}

func (d *JSONData) SetStream(stream interface{}) {
	d.stream = stream
}

func (d *JSONData) Mean() float32 {
	return 0
}

func (d *JSONData) Std() float32 {
	return 0
}

func (d *JSONData) Exist() bool {
	return d.stream != nil
}
