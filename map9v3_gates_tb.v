module map9v3_tb;

  /* Make a reset that pulses once. */
  reg start = 0;
  reg reset = 1;
  reg [8:0] N = 220;
  initial begin
     $dumpfile("map9v3_tb.vcd");
     $dumpvars(0,map9v3_tb);

     # 100   reset = 1;
     # 5000   reset = 0;
     # 5000   start = 1;
     # 5000   start = 0;
     # 40000 start = 1;
     # 5000   start = 0;
     # 50000 $finish;
  end

  /* Make a regular pulsing clock. */
  reg clock = 0;
  always #100 clock = !clock;


  wire [8:0] dp;
  wire [7:0] sr;
  wire [7:0] counter;
  wire done;
  map9v3 map9v3_inst(clock, reset, start, N, dp, done, counter, sr);

  initial
     $monitor("At time %t, counter = %h (%0d), sr = %h (%0d), dp = %h (%0d)",
              $time, counter, counter, sr, sr, dp, dp);
endmodule // map9v3_tb
