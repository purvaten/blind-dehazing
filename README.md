## Blind Dehazing Algorithms

This is an implementation of single image blind dehazing algorithms. We attempt to implement two papers, the ICCP '16 [paper](http://ieeexplore.ieee.org/document/7492870/) "*Blind dehazing using internal patch recurrence*", by Yuval Bahat & Michal Irani, and the CVPR '09 [paper](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5567108) "*Single Image Haze Removal Using Dark Channel Prior*" by Kaiming He, Jian Sun, and Xiaoou Tang.

The implementation of "*Single Image Haze Removal Using Dark Channel Prior*" is complete. Run it using `./start_dark_channel.sh`. Use the `--help` flag for a detailed list of arguments. Hyperparameters can be adjusted in `dark_prior/config/constants.yml`.

The implementation of "*Blind dehazing using internal patch recurrence*" is in progress.

## Blind dehazing using internal patch recurrence Results

### Transmission Maps
<p align="center"><img align="center" src="https://user-images.githubusercontent.com/13128829/38472254-f98ae5c6-3b9a-11e8-8dc4-38198c6668bf.png" width=800></p><br>
<p align="center"><img src="https://user-images.githubusercontent.com/13128829/38472256-024bdca6-3b9b-11e8-8c7a-01d943103df0.png" width=800></p><br>
<p align="center"><img src="https://user-images.githubusercontent.com/13128829/38472270-2866e048-3b9b-11e8-838a-d442b7440e2b.png" width=800></p><br>

### Results before tmap estimation (assuming lower bound on tmap)

<p align="center"><img align="center" src="https://user-images.githubusercontent.com/13128829/38472275-2f58c13c-3b9b-11e8-9942-589a213b23f4.png" width=800></p><br>
<p align="center"><img src="https://user-images.githubusercontent.com/13128829/38472279-3a66e400-3b9b-11e8-9385-b00f37e9c874.png" width=800></p><br>
<p align="center"><img src="https://user-images.githubusercontent.com/13128829/38472280-44152430-3b9b-11e8-9ff3-4ab937cd48ff.png" width=800></p><br>
<p align="center"><img src="https://user-images.githubusercontent.com/13128829/38472283-53c515fc-3b9b-11e8-8d0e-6332385b7765.png" width=800></p>

## Single Image Haze Removal Using Dark Channel Prior Results

You can find some results in this [report](http://home.iitb.ac.in/~kalpesh1729/report.pdf).
