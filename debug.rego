package main

deny[msg] {
  is_array(input)
  msg := sprintf("Input is array of length %d", [count(input)])
}

deny[msg] {
  is_object(input)
  msg := sprintf("Input is object with keys %v", [object.keys(input)])
}

deny[msg] {
  not is_array(input)
  not is_object(input)
  msg := sprintf("Input is type %v", [type_name(input)])
}
