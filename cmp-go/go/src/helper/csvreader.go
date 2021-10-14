package helper

import (
	"errors"
	// "fmt"
	"bufio"
	"encoding/csv"
	"os"
	// "strconv"
	//"github.com/gocarina/gocsv"
)

type CSVReader struct {
	data [][]string
	path string
}

func (d *CSVReader) Load(path string) error {
	dataFile, err := os.OpenFile(path, os.O_RDONLY, os.ModePerm)
	if err != nil {
		return errors.New("Not found csv data. (" + path + ")")
	}
	defer dataFile.Close()

	//targets := []*Target{}

	reader := csv.NewReader(bufio.NewReader(dataFile))
	rows, err := reader.ReadAll()
	if err != nil {
		return errors.New("CSV data could not be read. (" + path + ")")
	}

	d.data = rows
	return nil
}

func (d *CSVReader) GetData() [][]string {
	return d.data
}

func (d *CSVReader) Exist() bool {
	return d.data != nil
}
