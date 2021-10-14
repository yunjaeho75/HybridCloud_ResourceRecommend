package core

import (
	"os"

	"goml/helper"
	"goml/logger"

	tf "github.com/tensorflow/tensorflow/tensorflow/go"
)

func LoadSavedModel(path string) *tf.SavedModel {
	log := logger.GetLogger("engine")

	// load tf model
	tfModel, err := tf.LoadSavedModel(path, []string{"serve"}, nil)
	if err != nil {
		log.Error("%v", err)
		return nil
	}

	log.Info("Load model (%s)", path)
	return tfModel
}

func LoadData(handler helper.DataSet) [][][]float32 {
	log := logger.GetLogger("engine")

	err := handler.Load()
	if err != nil {
		log.Error("%v", err)
		return nil
	}

	log.Info("Load data (%s)", handler.GetPath())
	return handler.ToArray()
}

func ToTensor(data [][][]float32) *tf.Tensor {
	log := logger.GetLogger("engine")

	inputTensor, err := tf.NewTensor(data)
	if err != nil {
		log.Error("%v", err)
		return nil
	}

	log.Info("Convert data to tf tensor: %v", inputTensor)
	return inputTensor
}

func Predict(model *tf.SavedModel, input *tf.Tensor) [][]float32 {
	log := logger.GetLogger("engine")

	// actually get the prediction from the model
	run, err := model.Session.Run(
		map[tf.Output]*tf.Tensor{
			model.Graph.Operation("serving_default_bidirectional_input").Output(0): input,
		},
		[]tf.Output{
			model.Graph.Operation("StatefulPartitionedCall").Output(0),
		},
		nil,
	)
	if err != nil {
		log.Error("%v", err)
		return nil
	}

	log.Info("To completed th predction requested.")
	return run[0].Value().([][]float32)
}

func Export(data []byte, path string) {
	log := logger.GetLogger("engine")

	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		log.Error("%v", err)
		return
	}

	if _, err := f.Write(data); err != nil {
		log.Error("%v", err)
		return
	}

	if err := f.Close(); err != nil {
		log.Error("%v", err)
		return
	}

	log.Info("Write predict completed. (path=%v)", path)
}

// 데이터 표준화 함수
func Standardization(df [][][]float32, mean float32, std float32) [][][]float32 {
	for x, e1 := range df {
		for y, e2 := range e1 {
			for z, e3 := range e2 {
				df[x][y][z] = (e3 - mean) / std
			}
		}
	}
	return df
}

func Inverse_Standardization(pred [][]float32, mean float32, std float32) [][]float32 {
	// return pred*std + mean
	for i, row := range pred {
		for j, _ := range row {
			pred[i][j] = pred[i][j]*std + mean
		}
	}
	return pred
}
