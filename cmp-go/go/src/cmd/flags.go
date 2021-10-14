package cmd

import (
	"github.com/spf13/cobra"
)

type FlagsWrapper struct {
	cmd *cobra.Command
}

func (wrapper *FlagsWrapper) GetString(name string) string {
	if value, err := wrapper.cmd.Flags().GetString(name); err == nil {
		return value
	}
	return ""
}

func (wrapper *FlagsWrapper) GetInt(name string) int {
	if value, err := wrapper.cmd.Flags().GetInt(name); err == nil {
		return value
	}
	return 0
}
