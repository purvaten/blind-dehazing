## Blind Dehazing Algorithms

This is an implementation of single image blind dehazing algorithms. We attempt to implement two papers, the ICCP '16 [paper](http://ieeexplore.ieee.org/document/7492870/) "*Blind dehazing using internal patch recurrence*", by Yuval Bahat & Michal Irani, and the CVPR '09 [paper](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5567108) "*Single Image Haze Removal Using Dark Channel Prior*" by Kaiming He, Jian Sun, and Xiaoou Tang.

The implementation of "*Single Image Haze Removal Using Dark Channel Prior*" is complete. Run it using `./start_dark_channel.sh`. Use the `--help` flag for a detailed list of arguments. Hyperparameters can be adjusted in `dark_prior/config/constants.yml`.

The implementation of "*Blind dehazing using internal patch recurrence*" is in progress.

## Blind dehazing using internal patch recurrence Results

### Transmission Maps

![cone_tmap](https://user-images.githubusercontent.com/13128829/38472050-9a9bcc9a-3b97-11e8-8f17-83f4adf7e257.png)
![cityscape_tmap](https://user-images.githubusercontent.com/13128829/38472055-a5e674c4-3b97-11e8-951c-cc510b1bf85e.png)
![pumpkins_tmap](https://user-images.githubusercontent.com/13128829/38472068-eeea684c-3b97-11e8-8471-a96b3b47d72b.png)

### Results before tmap estimation (assuming lower bound on tmap)

![30074123_2054097438135437_1338466170_o](https://user-images.githubusercontent.com/13128829/38472071-fbcda600-3b97-11e8-84f6-9edea49c8927.png)
![30074586_2054095744802273_459964696_o](https://user-images.githubusercontent.com/13128829/38472075-081f869e-3b98-11e8-87ba-2b583b55ac12.png)
![pumpkin](https://user-images.githubusercontent.com/13128829/38472092-439b960e-3b98-11e8-85f6-9886384761a5.png)
![swan](https://user-images.githubusercontent.com/13128829/38472089-3a2c7782-3b98-11e8-952f-adb00d76dff6.png)

## Single Image Haze Removal Using Dark Channel Prior Results

You can find some results in this [report](http://home.iitb.ac.in/~kalpesh1729/report.pdf).
