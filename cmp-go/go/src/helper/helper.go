package helper

import (
	"errors"
	// "fmt"
	// "os"
	// "bufio"
	// "encoding/csv"
	"strconv"
	//"github.com/gocarina/gocsv"
)

type DataSet interface {
	Load() error
	ToArray() [][][]float32
	SetStream(stream interface{})
	SetFile(path string)
	GetPath() string
	Mean() float32
	Std() float32
	Exist() bool
}

func Get(format string) (DataSet, error) {
	if format == "time-series-base-csv" {
		return &CSVData{}, nil
	}
	if format == "time-series-base-api" {
		return &JSONData{}, nil
	}
	if format == "time-series-base-meta" {
		return &MetaData{}, nil
	}
	return nil, errors.New("This format is not supported. (format=" + format + ")")
}

func csvToArray(records [][]string) [][][]float32 {
	data := [][][]float32{}
	element := [][]float32{}
	for i, row := range records {
		for j := range row {
			v, _ := strconv.ParseFloat(records[i][j], 32)
			value := []float32{}
			value = append(value, float32(v))
			element = append(element, value)
		}
	}
	data = append(data, element)
	return data
}
