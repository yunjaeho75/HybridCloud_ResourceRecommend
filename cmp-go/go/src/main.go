package main

import (
	"fmt"

	"goml/api"
	"goml/cmd"
	"goml/core"
	"goml/helper"
	"goml/logger"
	"goml/util"

	"github.com/spf13/cobra"
)

func DebugFlags(flag *cmd.FlagsWrapper) {
	log := logger.GetLogger("main")
	log.Debug("--model: %v", flag.GetString("model"))
	log.Debug("--input: %v", flag.GetString("input"))
	log.Debug("--output: %v", flag.GetString("output"))
	log.Debug("--data-helper: %v", flag.GetString("data-helper"))
	log.Debug("--log: %v", flag.GetString("log"))
	log.Debug("--verbose: %v", flag.GetInt("verbose"))
}

func convertDataHelper(h string, format string) string {

	if h == "time-series-base" {
		if format == "consol" {
			return h + "-csv"
		}

		if format == "api" {
			return h + "-api"
		}
	}

	return h
}

func runConsol(flag *cmd.FlagsWrapper) error {
	log := logger.GetLogger("consol")

	modelFile := flag.GetString("model")
	dataFile := flag.GetString("input")
	helperType := convertDataHelper(flag.GetString("data-helper"), "consol")

	// load tf model
	tfModel := core.LoadSavedModel(modelFile)
	if tfModel == nil {
		return nil
	}

	// get data helper
	handler, err := helper.Get(helperType)
	if err != nil {
		log.Error("%v", err)
		return err
	}

	// load predict data
	handler.SetFile(dataFile)
	inputData := core.LoadData(handler)
	if inputData == nil {
		return nil
	}

	// apply normalization
	meta, err := helper.Get("time-series-base-meta")
	if err != nil {
		log.Error("%v", err)
		return err
	}

	metaFile := fmt.Sprintf("%s/meta.csv", modelFile)
	meta.SetFile(metaFile)
	core.LoadData(meta)
	if meta.Exist() == false {
		return nil
	}

	inputData = core.Standardization(inputData, meta.Mean(), meta.Std())

	// convert data to tf tensor
	inputTensor := core.ToTensor(inputData)

	// actually get the prediction from the model
	pred := core.Inverse_Standardization(core.Predict(tfModel, inputTensor), meta.Mean(), meta.Std())
	log.Info("Predict: %v", pred)

	// convert json from data
	doc := util.ToJson("None", pred)
	log.Info("%v", string(doc))

	// the result of prediction to export json
	core.Export(doc, flag.GetString("output"))
	log.Info("Completed.")
	return nil
}

func runApi(flag *cmd.FlagsWrapper) error {
	log := logger.GetLogger("api")

	modelFile := flag.GetString("model")
	helperType := convertDataHelper(flag.GetString("data-helper"), "api")

	// load tf model
	tfModel := core.LoadSavedModel(modelFile)
	if tfModel == nil {
		return nil
	}

	/// get data helper
	handler, err := helper.Get(helperType)
	if err != nil {
		log.Error("%v", err)
		return err
	}

	// get data helper
	meta, err := helper.Get("time-series-base-meta")
	if err != nil {
		log.Error("%v", err)
		return err
	}
	metaFile := fmt.Sprintf("%s/meta.csv", modelFile)
	meta.SetFile(metaFile)

	app := &api.App{}
	app.Create(tfModel, handler, meta)
	app.Run("0.0.0.0", "5000")
	return nil
}

func estimator(command *cobra.Command) error {
	flag := cmd.GetFlags(command)
	logger.SetVerbose(flag.GetInt("verbose"))
	logger.SetLogFile(flag.GetString("log"))

	fmt.Printf("log-path=%v\n", flag.GetString("log"))

	DebugFlags(flag)
	if command.Use == cmd.CMD_CONSOL {
		return runConsol(flag)
	}

	if command.Use == cmd.CMD_API {
		return runApi(flag)
	}

	return nil
}

func main() {
	cmd.SetUsageFunc(estimator)
	cmd.Execute()
}
