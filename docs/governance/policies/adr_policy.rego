package sdlc.governance

import future.keywords.in
import future.keywords.every

# Enforce ADR file naming
deny[msg] {
    some file in input.files
    not re_match(`^docs/architecture/design/adr-\d{3}-[a-z0-9-]+\.md$`, file.path)
    msg := sprintf("Invalid ADR naming: %s", [file.path])
}

# Ensure sequential numbering
deny[msg] {
    numbers := [n | file := input.files[_];
                matches := regex.find_all_string_submatch_n(`^docs/architecture/design/adr-(\d{3})-.*\.md$`, file.path, -1)
    count(matches) > 0
    num := matches[0][1]
                n := to_number(num)]
    unique_numbers := {n | n := numbers[_]}
    count(unique_numbers) > 0
    min_val := min(unique_numbers)
    max_val := max(unique_numbers)
    expected_count := max_val - min_val + 1
    count(unique_numbers) != expected_count
    msg := sprintf("ADR numbering is not sequential. Found: %v", [sort(numbers)])
}
