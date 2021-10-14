#!/bin/bash
exec go get
exec go build ./cmd
exec go build ./logger
exec go build ./helper
exec go build ./core
exec go build ./api
exec go build ./util
exec go install
