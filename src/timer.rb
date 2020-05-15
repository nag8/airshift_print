require 'time'
def timer(arg, &proc)
  x = case arg
  when Numeric then arg
  when Time    then arg - Time.now
  when String  then Time.parse(arg) - Time.now
  else raise   end

  sleep x if block_given?
  yield
end

# これがないとエラーになる。いつか直す
timer("24:00"){}

timer("08:00") do
  system("python shift.py")
end
  