header="avg_speed,cars_in_lane,spawn_chance,agression,min_gap"

for file in "$@"
do
    sed -i -e "1i\
$header" $file
done
