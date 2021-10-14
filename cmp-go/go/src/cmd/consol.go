/*
Copyright © 2021 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var CMD_CONSOL string = "consol"

var consol_logFile string

// consolCmd represents the consol command
var consolCmd = &cobra.Command{
	Use:   CMD_CONSOL,
	Short: "Run the predictive model using the Consol and return the predicted values.",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("consol-command\n")
		usageFunc(cmd)
	},
}

func init() {
	rootCmd.AddCommand(consolCmd)
	consolCmd.PersistentFlags().StringVarP(&input, "input", "i", "", "Specify the dataset to be used for prediction.")
	consolCmd.PersistentFlags().StringVarP(&consol_logFile, "log", "l", "estimator-ml.log", "Specify the location where the log will be saved.")
}
