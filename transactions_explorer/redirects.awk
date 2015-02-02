/Redirecting/ {
  print substr($12, 0, length($12) - 1) "\t"  substr($9, 0, length($9) - 1)
}

/Crawled/ {
  print substr($8, 0, length($8) - 1) "\t"
}
