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

var CMD_API string = "api"

var api_logFile string

// apiCmd represents the api command
var apiCmd = &cobra.Command{
	Use:   CMD_API,
	Short: "Run the predictive model using the API and return the predicted values.",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("api-command\n")
		usageFunc(cmd)
	},
}

func init() {
	rootCmd.AddCommand(apiCmd)
	apiCmd.PersistentFlags().StringVarP(&api_logFile, "log", "l", "estimator-ml-api.log", "Specify the location where the log will be saved.")
}
