package api

import (
	"encoding/json"
	"net/http"

	// "reflect"
	// "strconv"

	"io"
	"io/ioutil"

	"goml/core"
	"goml/helper"
	"goml/logger"
	"goml/util"

	tf "github.com/tensorflow/tensorflow/tensorflow/go"
)

var (
	tfModel     *tf.SavedModel
	dataHandler helper.DataSet
	metaHandler helper.DataSet
)

func predict(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	log := logger.GetLogger("api")
	log.Info("Call predict rest api.")

	// get json data from post
	body, err := HttpBodyToMap(r, 1048576)
	if err != nil {
		log.Error("%v", err)
		resposeError(w, err)
		return
	}

	// get data helper
	dataHandler.SetStream(body["sequance"])
	inputData := core.LoadData(dataHandler)

	// apply normalization
	core.LoadData(metaHandler)
	inputData = core.Standardization(inputData, metaHandler.Mean(), metaHandler.Std())

	// convert data to tf tensor
	inputTensor := core.ToTensor(inputData)

	// actually get the prediction from the model
	// pred := core.Predict(tfModel, inputTensor)
	pred := core.Inverse_Standardization(core.Predict(tfModel, inputTensor), metaHandler.Mean(), metaHandler.Std())

	// convert json from data
	doc := util.ToJson(body["label"].(string), pred)
	resposeMessage(w, doc)
	log.Info("Respose Message: %v", string(doc))
}

func resposeError(w http.ResponseWriter, err error) {
	log := logger.GetLogger("api")
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(422) // unprocessable entity
	if err := json.NewEncoder(w).Encode(err); err != nil {
		log.Error("%v", err)
	}
}

func resposeMessage(w http.ResponseWriter, msg []byte) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(422) // unprocessable entity
	w.Write(msg)
}

func HttpBodyToMap(r *http.Request, s int64) (map[string]interface{}, error) {
	body, err := ioutil.ReadAll(io.LimitReader(r.Body, s))
	if err != nil {
		return nil, err
	}

	if err := r.Body.Close(); err != nil {
		return nil, err
	}

	request := make(map[string]interface{})
	if err := json.Unmarshal(body, &request); err != nil {
		return nil, err
	}
	return request, nil
}

func install(a *App) {
	tfModel = a.Model
	dataHandler = a.Handler
	metaHandler = a.Meta
	a.Route("/ml/estimator", predict, "POST")
}
