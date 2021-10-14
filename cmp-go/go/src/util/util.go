package util

import (
	"encoding/json"
	"reflect"
)

func ToJson(label string, data [][]float32) []byte {
	dump := make(map[string]interface{})
	dump["label"] = label
	dump["predict"] = ToArray(data)
	doc, _ := json.Marshal(dump)
	return doc
}

func ToArray(data [][]float32) []float32 {
	dump := make([]float32, 0, 1)
	for _, row := range data {
		for _, col := range row {
			dump = append(dump, col)
		}
	}
	return dump
}

func InterfaceToArray(data interface{}) []float32 {
	dump := make([]float32, 0, 1)
	object := reflect.ValueOf(data)
	for i :=0; i < object.Len(); i++ {
		v := object.Index(i).Interface().(float64)
		dump = append(dump, float32(v))
	}
	return dump
}

func ToArray2D(records []float32) [][]float32 {
	element := [][]float32{}
	for _, row := range records {
        value := []float32{}
		value = append(value, row)
		element = append(element, value)
	}
	return element	
}

func ToArray3D(records [][]float32) [][][]float32 {
	element := [][][]float32{}
	element = append(element, records)    
	return element	
}
