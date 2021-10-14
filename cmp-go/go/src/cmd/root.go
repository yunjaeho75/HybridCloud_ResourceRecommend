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
	"os"

	"github.com/spf13/cobra"
)

var usageFunc func(*cobra.Command) error

var (
	model      string
	input      string
	helper     string
	logFile    string
	outputFile string
	// metaFile   string
	verbose int
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "goml",
	Short: "Run the predictive model and return predicted values.",
	Long:  ``,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	PreRunE: func(cmd *cobra.Command, args []string) error {
		if len(args) == 0 {
			cmd.Help()
			fmt.Println()
			os.Exit(0)
		}
		return nil
	},
	Run: func(cmd *cobra.Command, args []string) {
		if cmd.Use == args[0] {
			usageFunc(cmd)
		} else {
			cmd.Help()
			fmt.Println()
			os.Exit(0)
		}
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func SetUsageFunc(f func(*cobra.Command) error) {
	usageFunc = f
}

func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.DisableSuggestions = true
	rootCmd.PersistentFlags().StringVarP(&model, "model", "m", "", "Specify the predictive model to use.")
	// rootCmd.PersistentFlags().StringVarP(&input, "input", "i", "", "Specify the dataset to be used for prediction.")
	rootCmd.PersistentFlags().StringVar(&helper, "data-helper", "", "Specifies the data helper.")
	//rootCmd.PersistentFlags().StringVarP(&logFile, "log", "l", "estimator-ml.log", "Specify the location where the log will be saved.")
	rootCmd.PersistentFlags().StringVarP(&outputFile, "output", "o", "predict.json", "Specify the location of the model to be created.")
	// rootCmd.PersistentFlags().StringVar(&metaFile, "meta", "data/meta.csv", "Set meta information that can be used in the generated model.")
	rootCmd.PersistentFlags().IntVarP(&verbose, "verbose", "v", 1, "Specifies the level of log generation.")
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
}

func GetFlags(cmd *cobra.Command) *FlagsWrapper {
	return &FlagsWrapper{
		cmd: cmd,
	}
}
