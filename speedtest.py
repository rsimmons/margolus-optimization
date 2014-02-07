import time

import state

SINGLE_ROT_RULE_SEQ = (0, 2, 8, 3, 1, 5, 6, 7, 4, 9, 10, 11, 12, 13, 14, 15)
STRING_THING_RULE_SEQ = (0, 1, 2, 12, 4, 10, 9, 7, 8, 6, 5, 11, 3, 13, 14, 15)

import v1, v2, v3, v4, v5, v6, v7, v8, v9, v10

if __name__ == '__main__':
    # test_start_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=24&rle_y0=20&rle=bo4b3obobo$2b6o3b2o$8ob3o$4bobo5bo$3bob3o$bo2bobo4bo$ob5ob5o$4o2bob3obo$4b2ob2obobo$3ob2o2bo3bo$bob2obo3b3o$2o3bo2bobobo$b2o2b2ob2o2bo$3o2bob2obobo$bob3obobo2bo&step=1&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    # test_end_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=1&rle_y0=1&rle=15bo$5bo2$30bo$6bo52bo$o3$31bo2$15bo$35bo23bo$7bo31bo2$25bo$25bo17bo18bo$58bo$20bo$54bo2$25b6obo$22bo2b6o$29bo$4bo23b2o$27bobo$26b4o2b4o$21bo4bo2b2ob2ob2o$14bo12b2o2bo3bo9bo$27b2ob2o2b2o4bo$22bo4bo2b3obo$28bo2bobo$24b2o3bo2bo11bo$24b2o4b2o10bo$57bo$25bo$4bo$3bo$33bo3$31bo$38bo$45bo$25bo4bo8$25bo2$15bo$58bo$24bobo5$24bo2$32bo&step=1024&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    # test_iters = 467968
    # rule = SINGLE_ROT_RULE_SEQ

    # took about 10s in JS, or ~300 mega-cell-iters/s
    test_start_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,1,2,12,4,10,9,7,8,6,5,11,3,13,14,15&rle_x0=100&rle_y0=0&rle=2bo3bob5o2bob2ob2o2b2o3b2o3bo$o2b3obo3bob2obobo2bo2b2ob2ob3o$5ob3o3bobob5ob4o3bo4bo$2o2bobo2bo4b2o3bob2ob2o3b4obo$2b2o2b3o2bo4b2o2b2o2b2o2bobo$6b2obob2ob4o2bob4o2b4ob2o$2o2bob6o2b2ob8ob2ob2o$3ob3obobob3obobobob3ob3o2bob2o$ob2o5b2obobob3o5bo6bobo$o4bo3bob2ob5o4b2o3bo2b4o$4ob2obobobob3o2bobob2ob2ob4obo$2o2b2ob2ob3ob2obo2b2o2bobo3bobo$2o2b2o3b2o2b2o2b2obo5bo5b3o$2obo2bo3bob3o3b2o2b3obo3b2o$6b8ob2o2b2obobobo4bobo$2bo4bo3bob2o3bobo5b2ob2ob2o$3o2b2ob4o2b4ob3o2b2obob4o$2b2ob2obob2obobo2b7obob5obo$o2bo2b3ob2ob3obob2ob3o2b4o3bo$3o4b2o3b2obo4bo2b3ob2o$obobo2bob3obobo3bob2o3b4obob2o$o2b4ob6ob2ob4o4b3o2bo$2obobo2bo2bob7ob3o2b4o2b3o$2o2b3obob2obo2bo2b2ob2o3b2o2b4o$2bo2b3o2b7o3bo2bo5b2o2bo$2ob2o7b3o2b3ob2o3bo5bo$4b2ob3obobob2o2b3obo2bo2bo$2bo2bo3bo2b2o2bob2ob2o2bob4obo$bobob3ob2o5b2o4bobobob2o3b2o$2bobob2ob2o2b5obo7b4obobo$o6b2o2b2o4b2obo3b10o$3b3o3b3o2bobobo4b2ob5obo$2o2b2o4b3ob5o3b2ob2obob2o$7o3b2ob2ob2o5b3ob5o$bob2o2bo2bobob4o5bobo6bo$ob4ob2o2b4ob2ob2ob5obo4bo$3bo3bobobo2b3o3b7ob2ob2o$b3ob4obo6b2o2b3obobo3b2obo$2o2b2o2bobo2bobob2obo2bo2bo3bo2bo$obo2bo4bo4bo3bob2obo3b2obobo$obobob2ob3o3bo5bob3o3bo3b2o$b2o3bob2obo3bo3b4ob5ob5o$bo9b2o2bobo2b2o2bo3b3o2bo$obob4o3bobo2bob2o9b3o$b2obob2o2b2o2b2obo4bobo4bo2b3o$b5o3bo2bo3b2obobo5b2o3bobo$4b2o3bob7o5b3ob3o4bo$2o2bo2b2obo2bo2b2o2b4o3bobobo$2obobo2bobob2o4b2obo2bo3bo4bo$3bob3o4b3obobobo3b4o2b5o$o5bobo2bo9bobo2b5ob3o$3o3bo2bo2b2obo2bob2o5b5ob2o$2obob2obob3ob2o4b3o2b5obo$2bo3b2obo3bo3b2o2bo3b2o2bob2obo$bob6obobo2bob4o2b5obo4bo$o3b2o2b4obobo2bo2b3o6bo3bo$o2b4obo2bo6bo5bo2b2o2b4o$3o2bo2bo4b5obo2bob4obo3b2o$ob2ob3o7bob2obobo2b2o2bobo$bobo2bo2b2o6bob2obo5b5o$2bob2ob2obo3b4ob2o2bo3b2obobobo$o4b2ob2o3b4ob2ob3obo4b2o2bo$bob2o3bobo2b2obobo2bo3b2ob2obob2o$2b2o5bobobob3obob2ob2o4bo2b2o$obob2o2bo4bobo4bob3o2b3o3bo$3o2b2o3b5o4b5ob2ob2obob2o$b2obo2b5o2bob4o2b3obobo2bobo$bo2bobob2obo4bobob2ob3o4bo2b2o$obob3obo2b5ob2obo2b3ob3o2bobo$bo3b2ob2o2bob12o6b3o$ob2o3bobo2b3ob2obobob3ob5o$bobob3o2bo3bo2b2obob2o3b2obo$6o2b2ob2obob4obo4bo3b2o$ob2ob2ob3obo11b5o2b2obo$5o6bo4bo2b7o2b2obo2bo$o2b11ob2o4b2ob2o3b2o2b2o$2b5o2bob5ob3obo2bobo3b4o$4obobo2bobob2o5bo4bo3b3obo$2bo2bo3b2ob3obob2o4bo2bo2b4o$obob3ob3obobobo3bo4b2ob3ob3o$5obo3b2o3b2ob4o3bobo2b2o2bo$o4b2ob2o2b2o4bo2b4obobo3b3o$b2ob2obobob3o3bob3o3b2obo2b2o$3obo3bobo3bo5bob2obo4b3obo$b2obobo4b2ob2o6b3ob2o3bob2o$b2obob3obobo2b3obo4b4o2b2obo$b4o5b2ob3ob2o3bo2b3o3b2o$4obo2bobobo5bo4bo3bo2b3o$2ob2o2bo3bo3b6obo3b2obobo$2bo2bo5bobobob2obob3o2bo4bo$bo3b3o2b4obo2b2o2bobob2obo3bo$o5bobo3bo3b2o2b7o2bobobo$obo2bobo5b3o3b4o2b2o2b5o$o2bob2o3bob3o2b3o4bo4bobob2o$obo2b2ob3obo9b3obo3b2o2bo$bob2o2bo2b2ob3ob4o2bo4b2o2b3o$b2obob2o3bob3ob3ob2o2bo7b2o$4bo2b7obo4bo4bobo2bo3bo$2o2bob2o2b3o2bo2b3obo2b2o3bob3o$obob3obo3b2o2b3o2bob5obob3o$b3o2bobob2ob6o3b2o3b2o2b2obo$2b3o3bo4bo2b3o2b7o3b4o$4bo2b2o3b2o3bo2bobo2bobo2b5o$bobo6b3o2b3obob2o2b3o6bo$ob2ob3o2b4ob4ob5o2b2o2b3o$3ob4obob6ob2o4bo4bo$bo3b2o3b2o2bo3b2obo3b2o3bobobo$o6bobobob4o2b4o3b2obo3bo$4o2bo2bo4b2obo6b2o2bob2o$2b3o2b2o2bob2o2bo5bob3o4bo$ob2o3bo2b2obobo3bobo3b3obobo$bo2b2o5b2obo2bo2bo2bo4bo3bo$2o2b3obobobo3b3ob6o4bo$o2bo4b4ob2o3b3obo3bo2bo3bo$bo3bobo4bobob5obobo2bob3ob2o$b2o2bo4b2o4bo2b5obo3bo4bo$2ob2obobob2o2bob3o3bo2b5obobo$2o4b2ob3ob2o7b6ob3o2bo$o2bob3o2b2o3b2o2bo3b2o2bob2o3bo$bo4bo2bobob4obo2bo3b2ob3ob2o$b2o3b2obob2o2b2ob5obobo2b2ob3o$bobo5bob3o2bo4b2obo5b2o2bo$3obo2bo4bo2bo8b2o4b2ob2o$3b2o3b2o5b2o2bo4b2obo2b2ob2o$obo2bo6b4obo6b3o3b3obo$o2bobo3bo3b3ob4obobo6bob2o$2b2o4bobo3bo2b4ob5o2b5o$bo2bob2o2bobobob5obo4b6obo$2o2bo2bo7bo5bobo4bob2ob2o$4ob2o4b3o2b5o3bo7b2o$3o2b2obob2obob2o3b3obob2o5b2o$b2o2b2o3b2o3b2o5bob3obo3bo$o2bo2bobo4bobobobo2b2obo2bob3obo$3bo9b2o2b2obobo2bobo2b4o$3obo2b2o5bob2obobo3b3o2b2o$b2o2bob3o3b2ob2obob4ob5o2b2o$o3b2obo4bo2bob2o8bo$bobo2b2ob2obo2bobobob3o3bobo2bo$ob2ob2obo3bob4obob5obo4bo$ob3o5bobobo2bob3ob2obo2b4obo$2o2b4obo2bob8o4bo4b2obo$4obob4o2bobo5b2ob2o4b3obo$3ob2obo3b2o2bob4obo2b2o2b2o2bo$b2ob4ob3ob3obo2bobo2b2o2b2o2bo$o3bob4obobo5bob2o6b2o$o2bo2bo5bo3b2obobobo3b3o2bobo$2b3obo3b2o3b2o3bobo3b3obo3bo$4b2ob2o4b2ob2o4b2ob2obobob2o$bo3bobobo3b2ob3ob7ob2o3bo$3bobobo3b4ob4ob3o3b3o2b3o$4obo2bo4b4o3b2o2b3o6b2o$2o3b3o3bobo3b2o2bob2o3b2obo2bo$bo4b2obo5b4o4b4ob2o2b3o$3ob2o2b2ob2o3bo2b3o3b4o3b3o$6b4o2b3o3b3o2b4ob3obo$5b11ob2o3bo3bobo2bob2o$bo2bo3b2o4b4o4bobo2b4o2b2o$3bo3b2o2bo2bo2b2o2bo2b2o3bo$bob3obobob2o2b4o7b2obob4o$b4o2bo2b4o2b5o2bo2bob3obobo$bo3b2ob2ob2ob3o6bob2o2b3o2bo$8o3bob3ob2ob4o2bo3b2obo$7o5bo2bo3b2o3b4o2b3obo$obo4bo5b2o2b2o5bob2obo2bobo$6bo2bo3bob2obo3bo3b2o2bobobo$b7o2bobo2b2ob7obo7bo$2ob3o3b2ob2o9bobob3obo2bo$2o2b3obo2bob3ob2o2bo2b2obo3bo2bo$b2o2bo2b2obo4b3o2bo3bo2bo5bo$2ob2o2b2ob3o7b2o2b2o2bo3bobo$2bo4b2ob3obo3bo4b4ob4o2bo$4bobo4bob2o3b2ob2o3bobo3b3o$2obo4b5obo4b3o2b3o3bobobo$b2ob3ob3ob4obo4bo2bobobo3bo$o2bob10obo2b3obob5o2b3o$2ob4obo3b2o2bo2b4obobo2bo2b3o$5ob2obobo2b3obobobob2ob4obo$ob4obobobobo2bo2b4ob2ob2ob2o$b2o2b3o5b2ob2o3bobob2ob3obobo$b2o2b4obobo2b5o2b2o3b7o$4b3obo2b4o2bo2b8o2b3obo$b3o4bo4bo4bobo3bo2b3o$2o2b2o3bob2obo2b2ob2ob3ob2obob2o$b2obobo4b2o3bobo4bob5o2bobo$obobo2bo5b7ob2o6b3o$ob3obob2o2b2ob3o2bob2o3b7o$4o3b2o3b4ob2o2bob2ob2obob2obo$b2o7bo2bo4bob3ob6o3bo$bobo4bobo2bo2b6o3bobob3ob2o$o3b4obobo6bobob4o$3obo2bo2b3o3b4ob5ob3ob3o$2obo2b3o4bobo2b2obobob4o2bobo$b2ob3o5b2o4bob4obo2b2o$bobo2bobob2ob2o2bo2b2o3b2o3b5o$obo2b2ob2obob2ob6o3bobo2bobobo$2obo2bobobo2b3ob2o2b2o2b2ob2o2b2o$4obob3o3bobob5o3bob4o2bo$2obob4o2b6o4b2ob2ob2o3b2o$o2b2o2b3o2bo2b5o2b3ob3o3b2o$2bobo2bo2b3o2bob4o3b3o2b2ob2o$bob7o2b3o2bobobobo5bo2bo$b6ob3o3bob2obob3ob2o6bo$2o6bo6bo2b2obo5b5o$2o2bob4o9bob2o4b5o2bo$3bob4o2bobo5b3o5b4ob3o$obo2bo2bo5bob3obobobo4b2o2b2o$2ob2ob2obob3ob2o2bob2obobob3o$2bob2o3bob2obo2b2o2bo3bobobob4o$2b2o2bobo3b3ob3ob2ob2o2b2obo2b2o$o2bobobobob3o2bob2o7b2obobo$3o2b3ob3ob2obob2ob2obo3bo3b3o$obob2o2b2o4b3o3bobo3b2o2b5o$bo3b6obob7o3b3obo$b2obob2obob4ob3ob5obob2obo$3obobo3bob2o2bo3bo2b2ob2o2b3o$bob2o4bo2b2ob2obobob3o2bob4o$4obob5ob2o5b2obo3b2o3bo$obo3bo2b3o2bob4o2bobobob4ob2o$2b3o4b2ob3obobo5bobo2b4obo$o4bobobo3b5o3bob4o3b5o$3obob2obo2bobobob6ob4o2bob2o$obo6b2o6b2obo2b5ob4obo$obo2bob5o2b2ob3o5bo2b2o3bo$2obobo2b2o3bob6o3b4o2b5o$bo4b3obob2obob3o2bo2b3obob2o$2b3o2bob9obobob2o2bo3bo$2b3obo3b2ob2ob6obo2bo2b2o2b2o$3o2b2o6b4obob3o3b2ob3o$3obo3bo3b2o3bobob4ob5obobo$2b2ob2ob2obo3bobo2b2ob4o2bo2b3o$bobobo2b5obobob3o2b5o2b2o$ob2ob6obob2ob3obo3bo2b6o$b6obob2obo2bo2b2o5bobo2b4o$3b3o4b2o3b2obob2ob3o2b2obobo$3o3b5o2b2o5bo3b8o$3bob4o4bobo3bob2ob2o2bob4o$bob2o2bobo2b3o4bobob4o2bo2bo$ob3o3bo2bob2o2b4ob2o6b2o$obo6bo6b2ob2obob2ob7o$8b2obob2o2b3ob3o2b2o3bo2bo$b2o2bobo3bo6b6o3bo$b2obo5bo2bob3obob4o2b2o2bobo$b2o2bo3b3ob2o2bo2b6ob4o2bo$obob4o6b2ob2o2bo3b2ob4ob2o$obobob2obobo9b4o$2b5obobob4obob5o2b2obo2b2o$4o2bobo2bo5bobo2b2obo3bob3o$2ob2obo2bo2bob5ob2ob6o4bo$o3b3ob2ob5o2bo4b5o2bo$3bo3b2o3bo2b4obob2o3bobobobo$3o2b2o2bo4bo2b3ob2o3bo3bo3bo$2bob4o2bobo2b4o2bobobo2bo4b2o$bobobob2ob3o2b3obo2b4ob2ob3obo$2bo2b5ob5ob3o3bo3b4o2b2o$b5o3b3o3b2o2bo2bo2bob5ob2o$o2bo2b2o2b2ob2o2bobo2b2obo2bo2b4o&step=1024&frame_delay=10&size=256x256&cell_size=2,0&phase=0'
    test_end_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,1,2,12,4,10,9,7,8,6,5,11,3,13,14,15&rle_x0=61&rle_y0=0&rle=4bob3o23bo7bo5b2o7bob2ob3o2b4o5bob2o15bo4b3ob2o$5bo2bo21b3o6bo4b2o2b3o4bo7b2ob2o4bobo18bo4b3o5b2o$6b2o21bo11bob2o4bo8bo4b2o3bo10b2o13bo2bo8b2o$29bo12b2obo5bo4b4ob4o14bobo13b2o15b2o$30bo11bo6bobob2ob2o4bo6bobobo6b2o30b2o$30bob2o6bo5bo17b2o2b2o3bo20b2o$25b5obo2bo4bob3obobo2bobo3b3obo4bo5bo7b2o13b2o3b2o$25bo4bo4b4o3b2o5b2ob2o2bo3b2o3b2o5b2o5b2o15b2obobo$25bo4bo4b2o3b3obob3o5bo7bo4bo3bo24bobob2o$14b4o6bo6bo3b2o4bo9bo14b2o4bo23bobo$14bo2bo6b5o2bo7bobo3bo5bo3bob3o5bobobo13b2o11b2o$15bobo11bobo7bo6bo16bob3o2bo2bo9b2o$16b2o12b2o7bo9bob3o4b2ob2o5bo3bo12b2o$39bo8b2o7bo5bo4b2o2bo12bobo$40bob4o2bo7bo3bobobo3bo16bo2bo$18b2o25b2o2b2o2bo5bo4bo2bobo6b2o7b4o$18b2o24bo4bobo11bo2b2o4bo3b2o$18b2o19bob2obo3b3o4bo4bo$18b2o21bob3o2bo4bo3bo7b2o2bo2bo$40bo4bo10b2ob2o5bobo21b2o$31b2o8b2ob2o5bo4bo12bo2b2o15bo2bo4b2o$31bobo6b2o6b2o4bo4b2o23b2o3bo2bo4b2o$31bo2bo7b2obo6bo3b4o7bobo4bo9b2o4b2o$31bo3bo13bo2b3o4bobo3bob4o3bo$29b2obo2bo6b2o2bobob3o5b2o11bo7b2o$29b2o2b2o4bo2b2o6bobo3b2o2b2ob2o8bo4bobo5b2o2b2o$40bo4bo10bo2b3o3b2obo3bobo2bo2bo4bo2bobobo$26b2o10b2o3bobo9bo2b3obo2bobo2bo2bobobo2bo4bo2bo2b2o$17b2o7b2o9bo6b2o4bo7bobobo3bobo4b3o2b2o5bo2bo$17b2o18bo6bob2o2bo4bo4b2o3bo5bo2b8o2bo4bo$38b2obo3b3o2bo11bo6bo9b2obob3o2bo11b2o$24b2o4b2o6bo2bo10bobobobo6bo2bo2b2o6bob2o4b2o12b2o$23bo2bo3b2o6b3o7bo9bo3bo7b2o8b3o$23bo2bo16b2o4b2obobo2b2o2bo3b2obob2o4b7o7b2o$24b2o9b2o3b2obob4obobo2b2o4bobo2bob2o3b3o14b2o17b2o$16b2o12b2o3b2o2bo2bo4bo9b3o4bo6bo4b2o16b2o13b2o$15bo2bo11b2o7b2o6bo5bo2bobo4bo4bob2ob3obo15bobo$15bo2bo9b2o9bobo9b3o2bo8b3o8bo16b2o$15bobob2o7b2o12b2o3b2o3bo3bo4bo2bo3bo5b2o5b2o16b2o$14bobo2bobo12b2o6bo5bo7bo3bo5bo2bob3o7b2o16b2o9b2o$14b2o4b2o12bobo2b2obo2b5o5bobo2bo2bo2bob5o36bobo$18b2o15b2o5b3o3bo5bobo7bo2bo2b2ob5o6b2o23b2o$17bobo15b2o9b2o4b2o3bo4bo10bob3o6b2ob8o10b2o$16bo2bo15b2obo4b3obo2bo2bo2bo3bo5bo4bo2bo9b2obo2b2o2bo9bobo$16bo3bo16bo5bobobo3bobobob2obob2o2bo4bo12b2o2b2o2b2o10b2o$17b4o16bo6bo6bo3bobo2bobob3obo2b2o$23b2o4b2o6bo2b4o6bo2b2obo6bob2o5bo$23b2o3bobo6bobobo2bo6bo2b3o2b5o7bo$19b2o4b2ob2o7bobo3bobo8bo5b3o2bo4bo$19b2o4b2o3b2o5bo3bobo5bo2bo7bobo2bo3bob2o19b2o6b4o$30bobo5b2o5bo2bo3bobobob2o5bo23b3obo3b3ob3o$31b2o11bo2bo10bo4bo6b2o16bob3o4b4o$47bo3bo2bo4b3o3bo7bob2o11b2o$38bob2ob2obo3bo9bo4bo4bo3bobo25b2o$25b2o10bo4bo3bo7b3obobob2o3b2o3b2obo19b2o5b2ob2o$25bobo9bobobo3bo3bo3bo4bobo2bo2b2obo2b3ob2o12b5obo7bobo$21b2o3bobo8bo2bo4b3o3bob2o2bo9b2ob2o3bobo12bo5bo7bob3o$21b2o4b2o8b4o7b2o2bo2b2o2bobo2b2o9b2o14b3o3bo6bo3bo$39bobo7bob3obo6bo6bobobo20b4o6bo2bo$41bo2bobo2b2o5bobo4b4o6bo31bobo$39bobo2b2ob2o9bo6bo2bobo35b2o$43bobo2bo3bo9b7obo$41bobo6bobobo3b4o3bob5o3b2o$26b2o12bo5bo3b2o7bob2ob2o4bo3bobob2o6b2o$17b2o6bobo14bo3bo5bo5b2obo13bobobo5bobo$17b2o6b2o5b2o6bo3bo3bo6bo2bo4bo2bo3bobobobobo6bobo$21b2o9b2o7b3o3bo8bo6bobo2bobobo3b2o8b2o$20bobo9b2o2b2o4b3o3bo4b3o7b2obo$20b2ob2o7b2o2bobo4bo9b3o4bo8bo3b2o4b2o$23bobo10bo12b2o3bo3bobo3b2o8bo3bobo$17b2o5b2o9bo3b2o2bo3bo4bo4b5obo3b2o8bobo$17b2o16bo4bo2bo3bo3bo2bob2o4b2obobo2bo6b2o$36bo5bo5bo4bo7bo2b2o$14b2o12b2o6bo3bo3bo6bo2bo3bo3bobo4b2obo$13bobo5b2o5bobo5bo6bobo8b2o6bobo3bo6b2o$8b2o3b2o6b2o6b2o5bo6b2o3b3o2b2o9bobo3bo2bob2o21b2o$8b2o7b2o17b3obobo2bo4bo3bo6bo5bo3bo26bobo$17b2o9b2o12b2o2bo5bobo3bobo2bo3bo3bo27b2o$28bobo2b2o9bo3bo6bo2b5o4bo5bo21b2o$22b4o2bobo2b2o4bo2bo4bobo2bobobo7b3o2b2o3b2o19b2ob2o$21bo4b2obo14bo3bo2b2ob2o4bo2bo5bo4b2o22bobo$21bo6bo13b2o2bo2b2o5b2o5b3o7bo4b2o18bo2bo$21bo6bo16bo2b2o8bob3o3bo2bobo6b2o18b4o$21bo2b2o2bob2o7bo10b2o5bo6bo6b2o$22b2o2b2obobo7b2o2b3o2bob3obo2bobo4bo5bo4b2o20b2o$28bobo3b4ob2o2bo7bo9b2o6b2o2bobobo19b2o$28b2o3bo4bo2bobo3bo2bob2o2bo4bobo3b3ob3o2bob3o$33bo7bo3bo5bo2bob4o6bobo2bo4bo3bo$34bo13bo6bo2b3o8bo6bo2bo$34bob2obo4bo2bobo3bo5b2o3bo12b2o$19b2o2b2o9bob2ob2ob2o4bo2bo2b2o2b2obobobobo$19b2o2b2o10bo2b2o4bo7bo17bo$36b2obobo5bo4bo5bo2bobo8bo$14b2o18b5o3bobo3bobobo2bo4bo7bobob2o$14b2o17bo8b2o4b2o4bo4bob2o2bob2o5bo$33b3o2bo7b2obo9bo2b2o5bo3b2o$36b2o5b2o2bo3b2o7bob5o3bobo$43bo16bo7bobo$44b2o3b3ob2o5b2o5bo2bo$30b2o13bo5bo3b2o16bo20b2o$30bobo9bo2bo11b2obobo2bo6bo12b2o7b2ob2o$20b2o9b2o7bo8bob2o2b2o2bo2b2ob2o18b2o10b2o$20b2o17bo5bo4bobo3b2obo5bo3bo17b2o$30b2o6bo2bo3b4o10bobo2b2o4b3o13bobo$30b2o6bo4bo8bo10bob2obo2b2obo11b2o$12b2o10b2o13b2o2b5o8bo8b2o4bo3bo$11bobo10b2o7b2o4bobobo2bo3bo3bo2b3o5bobo2bo3b2o17b2o4b2o$11b2o11b2o7bobo7bo6bo2b2o4bobo12b2o2b2o13b2o4bobo2b2o$24bobo7bob4o4bo7bo5bobo2b2o6bo2b2o2b2o20b2o2bobo$25bobo7bo3bob2ob2o3b2o4b3obob2o6bobo20b2o11b2o$26b2o7bob2o2b2o2bo2b2o5bo5bob2o2bo24b2o$35b2o3bobo3bobobo6b3o5bobob3o$41bo3b2o2bo4bobobo2bo4bo2bo$28b2o15bobo6b2o6b2o2bobob2obo14b2o6b2o6b2o$27bo2bo11b2o4bo2b2ob2o5bo3bobobo2bo15b2o5bobo6b2o$27b3obo8bo5bo3bo5b2o12bo17b2o5b2o$21b2o7bobo15b2o4bo2bo3bo6bo2bobo3b2o9b2o$21b2o7bobo7b4o4bo3bob3o4bo2b3o3bobo4b2o11b2o$30bobo9bo11b2obo7bo6bo14b2ob2o$14b2o14bobo6b2o3bo2b3o9bobo2bo3b2obobo13b2o$14b2o5b2o7bobo9bob2ob2obo2bo4bo4bo6b2o3b2o24b2o$21b2o8b2o7bo3bo3bobo4b2o2bo2bo2b4o3bo2bobo23bobo$41b2o2bo5bo2b2o8b3o4b2o3bobo22bobo$30b2o7bobo3bo2bo6bo2bo12bobo2bo2bo20bobo$30b2o9bo3bo2bo4bo2bo2b4o4b4ob2obo3bo19bobo$42bobo5bobo6b2obo4bobo2bo2bo2bo15b2o2bobo$40b3o10bo10b2o8bob2o16b2o2bobo$22b4o14b2obobo5bob2o5b2o6b2o4bob2o2b2o17b2o$13b2o7bo2bo16b2o3b3o9bo2bo3bo2bo3bo2b2o2b2o$13b2o8b2o11b5o11bob2o3bob2ob4o4b2o$35bob2o3bo5b2o9b2obob4o$34bobo5bo4b3o3b3o7bobo5bo26b2o$15b2o17b2o5bo2b4o2bobo2bo2bo3b3o7b2o24b2o$15bobo18b2ob2o4bobo3bo5b2o4b2o$16bobo17b2o3b2obo4b4o3bo4bo3bo3b2o$17bobo18bo2bo2b2o8b2obo2b2o4bo3b2o24b2o$17bobo17bo8bo7bo2bo3bobo5b2o2bo5b2o15b2o$14b3o2b3o15b2o2bo2b2obo7bo3b2o12b3o2bo2bo8b2o$14bo6bo3b2o8b2o10bo2b4o5b2o6bo8b2o3bo8b2o$15bo5bo3b2o3b2o2bobo3b3o6bo20bo2bo7bo$16bo2b3o8b2o2b2o7bo3bo6b2obo3bobo3bo5bo7bo$16bobo17b2o2bo2bobo3b2o3bo2bo6b2obobo3bo4b2obo$16b2o7b2o9b2obobo3bo7bobobo19bo2b2o9b2o$25b2o14bo8bo2bobo3bo17bo13b2o$43bo4bo4bo4b2ob3o2b3o3bo4bo13b2o$26b2o14bo5b2o5bobo4bob4o3bo4bo14b2o$25bo2bo10bo3bo4b2obo2bo6bobo2bo3bo2b2obo2b2o12b2o$25bo2bo10bobo7bo7b2obo3bo3b2o3b2obo2b2o5b2o5bobo$26b2o14bobo5bo6bo2bo11bo3bo9b2o6b2o$16b2o22bo4bo2bo2bo2b3ob2obobo3bo2bo6bo22b2o$16b2o22bobo7bo4bobo4bobo2bobobo6bo20bobo$44bo7bo2bob2o5bo7bo5bo19bobo$5b2o32bo8b2o3bob4obo4bob2ob2o5bo20b2o$5b2o34bobo8bo3b3o5bo5b4o2bo19b4o$11b2o14b2o6b6o2bo5bo3bo4b2o2b3ob2o3bo4bo18bo3bo$11bobo13b2o6bo2b2obob2o6bobobobo2bo9bo6bo17b4o$12b2o22bobo2bo9bobob2o2bo4bo3bobo4b3o17b2o$36bo2bo7b2o3bo2bo2bo11bo4bo14b2o3b2o$36bo4b4o4b4o5b2o11b3obo14bob3o2b2o$37bo10bo6bo2b2o3bo4bo3bo2bo15bo3b2o2bo$37bo9bo2b2ob2o3bo10bo6bo6b4o4bo7bo7b2o$26b2o9b2obo6b2obo13bo12bo5b4o4bo4b3o8b2o$3b2o21bobo4b2o2b2obo5bo7bobo3bo3b2o5b3o4b3o11bo3b3o$3b2o22b2o4b2obo2bo2b4o4bob5o4bo2bo15bo3b2o6bob2o3bo$11b2o4b2o16bo5b2o2bo2bobobo4b4o7bob3o7bo3b2o6bob2o3bo$10bobo3bo2b5o4b2o5b3o3bobo3b2ob2o4bo10bo3bobo6bo12bo4bo$10b2o4bo2b5o4b2o8b2o3bo3bobo4bo6bo5bo2b2obo6bo12bo3bo$6b2o9b2o9b2o15bo2bo3bo16bo3bo2b2o2bo12bo2bo$6bobo19b2o9bobobob2o9bo7b2o2bo2b3o2b2obo14b2o$2o5b2o7b2o24bo7bo4b2obo3bo6b3o6bo11b2o$obo13b2o13b2o8bo2b3o2bo3bo3b2o6bo2bo6b3o3b2o6bobo$b2o28bob3o6bo2bobo3b3o3bo2b2o6bo4b2o5bobo6b2o$32bo2bo3b2o3bo3bobo3bo4b4o7b2o8b2o$8b2o22bobo5b2o2bo4bo3bo2bobo6b2o3bo3b2o16b2o$8b2o22b2o5bo2bo3bo9bo8bo2bob2o4bo10b2o3bobo$39bobo2b2o2b2obobo3bo2bo8bo2b5o10b2o4b2o$40bo7bo2bo2bo3bo5bo2bo5bo13b2o$40b2o4b2ob2o5bo4bo2bobo2bo3bo12bobo$39bo4bo4bo4bo2bo2b2o3bobob3o14b2o3b2o$28b4o7bo4bobo4bo7bo4bo4b2o20bobo$28bo2bo10bo2b2o4b2o3b4o4b2o5bobo18b2o$29b2o12bobobo2bob2o6b2ob3obo2bo13b2o$40bo3b2o2bo2bo3bo3b2o2bo2bo17b2o$14b2o23bo11b2o3bo7bo2bo$14b2o23bo3b2o4bob2o5b2o3b2o7b2o17b2o$14b2o20b3o17bo4bo3b3o2bobo13b2o3b2o$13bo2bo2b2o15bo2bob2obo2bo6bo2bo3b3o2bo6bo12bobo$13bo3bob2o15bo4bo2bobo2b2obo6bo3b2ob2o5bo13b2ob2o2b2o$13bo3bo18bo4bobobo2b4o6b2o2b2o5b2o19b2obo2bo$12bo4bo19b2o4bobo5b2obobo2bo4b3o2b3o21bo2bo$12b3o2bo21bobo5bobobobo2bob2o3bobo4b2o22b2o$15b2o15b2o5bo4bo3b2obo8bo5b2ob2o11b2o18b2o$31bobob4o5bobo3bo2bo4bo2bob2obo3bobo9b2o18b2o$30bo2bobo3bobo6bobo7bo11bobo$30bo3b2o3bo2b2ob2o9b2o23b2o$31bo2b5o4bo2bo3bob2o7bo2bo5b4o7b2o19b2o$32b2o7bo3bo2b4o3b2ob2o4bo6bo2bo2b2o23b2o$14b2o32bob2obo3bo3bobobo4b2o2bo2b2o$13bobo24b3o2bo10b2obob2o7b2obo15b2o$13bobo14b4o5bob4obo3bo3bo7b2obo7bo15b2o3b2o$14b2o13bo3bo7b3ob2o3b2o2bo2bo5bo6bob2o5b2o8b2o3b2o$29bo2bo11bo3bobobo4bo3bobo2b3o3bo6b2o8b2o$30b2o8b4o2bo4bo9bo3bob2o$22b2o16b3obo3bobo3bo2bo2b2o2bobo2bo2bo$21bobo15bobo2bo6bo2bo2bo5bo2bo2b3o$20bobo9b2o4b5o4bo6b2ob2o3b4obobobo$20b2o10bobo2bobo7bobo3bo5b3ob2o4bo3bo11b2o$33b2o2bo2b2obo5bo2bo5b2obo2bo7bob2o9b2o$37bobo4bobo9bob5obo4b2o2bobo$37b3ob4obo2b2o2bo7bob2ob2obo3b2o31b2o$39b2o6b3obo3b2o2bo3bo4bo2bobo31bobo$20b2o17bo2bobobo2bo2bo3b3o2bo3bo7bo31b2o$20bobo16bo5bo22bo2b4o26b2o$21b2o16bob2o3bo2b2o2bobo2bo4bobo2b2o4bo21b2o3bobo$33b2o2b2o4b2o3bo11b2o2bo2bo3bo2bo12b4o5b2o4b2o$32bobo2bo3bo2b2o3b3o3bobo2bo6b2o2bo3bo11b3obo2b2o$32b2o3bobo3bo4b3o2b2o7bobo4b3o3bo14b2o2b2o5b2o$37b2o2bo4b2o2bo11bo3bobo6b3o14b2o7b2o$40b3obo3bo2b2o2bo2bo6bo12bo13bobo$39b2o2bo3bo5bo5b2o2bo4bo3bob2o2bo9b2o2bo2bo$40bobob2o2b3o4bo3bo2bo3bo3bo2bo2b2o9bo2b2o3bo$45bob2o4bo3bo10b2o16bo5b3o$29b2o12bo3bobo4bo4bobobo5bo4bo11bo2b2obo$14b2o13b2o19bo5b2o3bo3bo2bo3bobo9b2ob2o2b2o$14b2o23bo2b2o3bo3bob2o3b2o4b2o4bo13b2o$32b2o5bo4bo3bo7bo5b2o2b3o7b2o$32bobo4bob3o7bobobobobo2bo2bobob2ob2o2bobo2b4o$18b2o13b2o10bo3bo3b3o4bob2ob3obo7b2o2bo3bo$17bo2bo10b2o15bob2ob2obo14bobo7bo3bo9b2o$16bo4bo9b2o6b2o16bo2bob2ob4obo9bo3bo10b2o$16bo4bo5b2o10bo2bo3bo3b2o5bob2ob2obobo2bo3bo4bo3bo$14b3o3bo6b2o13bo2bo4bo3b4o6b2obobo2bobo4b4o$14bo4bo19b3o2bo3bo2b2obo14b2obo$15bo2bo20bo6bo2b2o5bo2bobo$16b2o3b4o14bo3b2ob3obobo4bo12bobo$21bo2bo13b2o9b2o3bo2bo4b3o2b2o13b2o$13b2o7b2o14bo7bo2b2ob2o4bo3bo2bo6bo9b2o13b2o$13b2o32bo2bo3b2o8bob2o4bo23bobo$42b2o4bo2bo3b2obo2bobob3ob2obo23b2o$38bobob2o2bo2bo2b2o2b2o4bobobobob2ob3o26b2o$37bo12b3o4bo2bob2o3bo4b2o2bo2b2o21b2o$37bo5bobob2o2bo4bo2bob2o8b2o3bo2b2o3b2o$31b2o4bob2o2bobo2b2obo6bo5bo2bo5b3o8b2o3b2o$31b2o3bo5b2o2bo6bobobo3bo8bo18b2o$36bo5bo2bo2b2o4bo7bo3bo2bobobo11b2o$24b2o6b2o3b2o18bo6bo9b2o9b2o$23bo2bo5b2ob2o16b2o2bo11bo4b2o21b2o$23bo2bo8b2o4bobo2bo2b3o3bo7bobo2b4o25bob3o$23bobo13bo6bobobo5bo7b2o4bo26bo3bo$23b2o3b2o2b2o21bo3b2obo10bo14b2o7b4o$25b2obobob2o3b2o5bo6bo6bo2b2o4bob2obo10b2o2bo2bo$10b2o12bo2bob2o5bob3o2bob2o5bo13b2o3bo10bobobo3bo$9bobo12b3obo6bobo2bo5bob2obo7bo2bobo3bo3bo9b2o2b4o$9b2o16b2o5bobo3bobo2bobo2bo4bobobobo2b2o2b2o4b2o30b2o$13b2o18bo2bo6bo2b3o5b2o3bobo3bobo6b2ob2o27b2o$4b2o7b2o17bo4b2o8bo8bo2bob2obo6b3o2bobo15b4o4b2o&step=1024&frame_delay=10&size=256x256&cell_size=2,0&phase=0'
    test_iters = 45056
    rule = STRING_THING_RULE_SEQ

    test_start_state = state.parse_dmishin_url(test_start_url)
    test_end_state = state.parse_dmishin_url(test_end_url)

    # print format_state(test_start_state)
    evolve_modules = [
        v1,
        v2,
        v3,
        # v4,
        v5,
        v6,
        v7,
        v8,
        v9,
        v10,
    ]

    for mod in evolve_modules:
        t0 = time.time()
        end_state = mod.evolve(test_start_state, rule, test_iters)
        dt = time.time() - t0
        # print format_state(end_state)
        assert state.states_equal(test_end_state, end_state)
        print '%9d mega-cell-iters/s - %s %s' % (int(test_start_state['width']*test_start_state['height']*test_iters/dt/1e6), mod.__name__, getattr(mod, 'description', None) or '')
