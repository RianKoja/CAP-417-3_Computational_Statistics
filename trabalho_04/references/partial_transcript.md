
# CongNaMul: A Dataset for Understanding the Growth of Soybean Sprouts

***

## Abstract

*(Not explicitly extracted — content begins directly with the introduction sections below.)*

***

## I. Introduction

### A. Smart Agriculture

### B. Soybean Sprouts as a Key Agricultural Product

### C. The Need for Automated Measurement

It is physically impossible to measure each of the millions of soybean sprouts individually, and even sampling surveys take a considerable amount of time. It took approximately six hours to measure the weight of 500g of soybean sprouts and the head length, body length, body thickness, and tail length for the creation of the dataset. Therefore, the development of technology to automatically measure the results of soybean sprout cultivation is absolutely necessary. 

### D. The Absence of Soybean Sprout Datasets

There were no data-driven analyses or available datasets related to the cultivation of soybean sprouts. Various studies have been conducted on soybeans themselves. For instance, Yang et al.  proposed a dataset for semantic segmentation on soybean pods. Wang et al.  proposed cultivar recognition through pattern analysis of soybean leaf image data. Abade et al.  proposed an AI model that distinguishes nematodes that infect soybeans, and Griera et al.  proposed a deep learning technology to estimate soybean production. However, there are no sophisticated datasets related to soybean sprouts, leaving industry practitioners without resources to reference for research, making an AI-based approach on soybean sprout production much more difficult. 

### E. Necessity of a New Dataset for Advanced Analysis

Considering the substantial demand for soybean sprouts in Korea and the global consumption of mung bean sprouts, which can be cultivated similarly, there is an undeniable advantage to applying advanced analysis to soybean sprout images. Therefore, the creation of a sophisticated image dataset using soybean sprouts is crucial. 

The authors constructed a fundamental dataset by photographing soybean sprouts on a large scale and through manual labeling, then generated a significant number of augmented images and mask labels through combination of each image. The resulting dataset, **CongNaMul**, supports:

- **Classification** — distinguishing whether there are diseases, spots, or broken stems for quality control
- **Semantic segmentation** — for precise analysis
- **Image decomposition** — for separating individual sprouts from group photos
- **Physical feature measurement** — automated estimation of morphological dimensions 

***

## II. Method

### A. Raw Image and Physical Feature Acquisition

All photos were taken using the default camera app on the **Samsung Galaxy S22**, resulting in **3,024 × 3,024 JPEG** format images. Photos were taken with bean sprouts placed on the ground, with the camera lens fixed at a height of **30.5 cm** from the ground. 

Photos were taken against **three types of backgrounds**:

- **Clear background** — natural setting; can be difficult for robust model training alone
- **Green checkered background** — green contrasts with the color of bean sprouts and is commonly used on industrial conveyor belts in Korea; grid at 5 mm intervals
- **White checkered background** — common on food conveyor belts; relatively harder to distinguish since sprout bodies are also white; grid at 5 mm intervals 

Each bean sprout was re-photographed against all three backgrounds. Additionally, multiple-sample images were taken with **five bean sprouts randomly placed** in one shot. After photographing, physical features were measured: **weight** (electronic scale) and **head length, body length, body thickness, and tail length** (vernier caliper). 

A total of **205 bean sprouts** were photographed (45 missing weight measurements). Since each was photographed on three backgrounds, **615 single bean sprout photos** were collected. For multiple samples, **3,690 multi-sample images** were collected. After removing out-of-focus images, **604 single samples** and **1,030 multiple samples** remained. 

### B. Semantic Segmentation Dataset Production

**Labelme**  was used to segment the captured images. Objects were labeled into three classes — **head**, **body**, **tail** — with remaining areas automatically labeled as **background**. Labeling results were output in **JSON format** (polygon coordinates) and also converted to **palette mode PNG files** (values 0, 1, 2, 3 for the four classes). 

Both formats are available for download. The PNG format is directly usable as input labels for semantic segmentation training (e.g., with TensorFlow's `sparse_categorical_crossentropy` loss). 

### C. Image Cropping with Segmentation Mask Analysis

By analyzing the pixel distribution of the labeled masks, images were cropped to the smallest size that still fully represented each soybean sprout. The longest sprout was found to occupy **2,016 px** in one direction; single sample images were therefore cropped from **3,024 × 3,024 px** to **2,016 × 2,016 px**. Multiple sample images were cropped to **2,675 × 2,675 px**. This eliminates unnecessary areas, enhancing training efficiency and reducing VRAM usage. Uncropped original images remain available for download. 

### D. Image Decomposition Dataset Production

In industrial settings, soybean sprouts are processed in bulk — hundreds of thousands at a time — making it impossible to photograph each one individually. To address this, an **Image Decomposition Dataset** was created by combining two images into one new image, simulating real factory conditions where sprouts are tangled or overlapping. 

The production pipeline involved three steps:

1. **Preprocessing** — Contrast Limited Adaptive Histogram Equalization (**CLAHE**)  was applied to all images to equalize pixel value distributions, reducing artifacts from bright backgrounds and light reflections.
2. **Mask synthesis** — Two palette PNG masks were loaded as NumPy arrays of size (2016, 2016). A new mask was created by taking the element-wise maximum of the two arrays. (Limitation: class 3 always covers classes 1 and 2; class 2 always covers class 1.)
3. **Image synthesis** — Pixel values were converted from `uint8` to `float32`, and a new image was created by computing the **pixel-wise average** of the two images. 

Only images from the **same background pattern** were combined. The number of synthesized images follows the combinatorial formula \( \binom{n}{2} \):

- Clear background: **19,900** images
- Green checkered background: **20,706** images
- White checkered background: **19,900** images
- **Total: 60,506 images** 

Due to storage constraints, the dataset is provided as **source image files and generator source code** (not raw files). The generator produces `.npy` (NumPy binary) files. The binary structure is:

- Images array: `(width, height, RGB, 3_images)`
- Masks array: `(width, height, 3_masks)`

Images and masks are sorted by non-zero mask area (ascending). The image with the smaller mask area is placed in the front channel; the larger in the back. The synthesized (input) image is in the last channel. Ground truth outputs are at indices `[..., 0]` and `[..., 1]`; the model input is at index `[..., -1]`. 

### E. Classification Dataset Production

Single bean sprout photos were directly classified into **four categories**. An additional **1,385 photos** were taken to balance classes, resulting in **500 photos per class** (2,000 total). All photos are **3,024 × 3,024 px JPEG** files with no preprocessing applied. 

| Class | Description |
|---|---|
| **Normal** | Highest quality, no damage |
| **Broken** | Body (hypocotyl) is broken — industrially undesirable; broken tails are acceptable |
| **Spotted-head** | Black spots on the head (cotyledon) — most fatal defect as visible after cooking |
| **Broken + Spotted** | Individuals exhibiting both defects |

### F. Physical Features Prediction Task

Physical feature information (head length, body length, body thickness, tail length, weight) is provided in **JSON format** for all individuals in the Semantic Segmentation and Image Decomposition datasets. Researchers can look up values by individual filename. 

The JSON schema is:

```json
{
  "filename": {
    "length_head": Number,
    "thickness_body": Number,
    "length_body": Number,
    "length_tail": Number,
    "weight": Number
  }
}
```

All length values are in **millimeters (mm)** as floats; weight in **milligrams (mg)**. Samples missing weight measurements are marked with `-1`. For multiple-sample images, physical features of all five sprouts are provided together without mapping to specific objects in the photo. 

***

## III. Dataset Statistics

The complete dataset statistics are summarized below (no augmentation applied): 

| | Semantic Segmentation (Single) | Semantic Segmentation (Multiple) | Decomposition | Classification |
|---|---|---|---|---|
| **Number** | 604 | 1,030 | 60,506 | 2,000 |
| **Size 1** | 3,024 × 3,024 | 3,024 × 3,024 | Image: (Xdim, Ydim, 3, 3) / Mask: (Xdim, Ydim, 3) | 3,024 × 3,024 |
| **Size 2** | 2,016 × 2,016 (cropped) | 2,675 × 2,675 (cropped) | Free resizing available | 1,024 × 1,024 |
| **Size 3** | 1,024 × 1,024 | 1,359 × 1,359 | — | 512 × 512 |
| **Size 4** | 512 × 512 | 679 × 679 | — | 256 × 256 |
| **Size 5** | 256 × 256 | 340 × 340 | — | — |
| **Format** | JPEG (image) / PNG palette (mask) | JPEG / PNG palette | Generator source code (.py) + .npy | JPEG |
| **Physical Features** | Yes | Yes | Yes | No |
| **Classes** | 4 | — | — | 4 |

Simple augmentations (vertical/horizontal flips, 90° rotations) can easily multiply dataset size by 4× or more. 

***

## IV. Application Strategies

- **Semantic Segmentation Dataset** can train preprocessing models that distinguish sprout parts (head, body, tail) from images. Combined with physical feature labels, it can also train end-to-end models that predict physical characteristics directly from pixel distributions. 
- **Decomposition Dataset** is essential for developing models usable in real industrial environments, where individual sprout photos are impractical to collect. A model trained on this dataset learns to decompose a multi-sprout photo into individual sprout photos. 
- **Classification Dataset** can train CNN-based classifiers for quality control. With simple augmentation, an efficient model suitable for deployment on mobile devices is expected to be achievable. 

***

## V. Conclusion

The **CongNaMul** dataset facilitates development of various AI technologies needed in bean sprout production, enabling training of models for quality control across multiple tasks. 

A noted **limitation** is dataset size: while the Decomposition dataset is sufficiently large, the single-sample segmentation data is small and requires augmentation during training. Future work to create a larger dataset is encouraged. 

The key **advantage** is data accuracy: beyond conventional human-labeled segmentation masks, the dataset includes physical features measured directly by human researchers, supporting reliable and trustworthy AI model development. 

***

## Acknowledgment

The authors express gratitude to **Seung Yeop Jang, Tae Dong Eom, Changyul Lee, Minwoo Lee, Yeongbeom Kwon, and Junsan Kim** for their invaluable assistance in the semantic segmentation labeling of soybean sprout images. 

***

## Supplemental Data

Dataset and overlapping code are available at: **https://bhban.kr/data** 

***

## References

1. Ban, Byunghyun, and Soobin Kim. "Control of nonlinear, complex and black-boxed greenhouse system with reinforcement learning." *2017 International Conference on Information and Communication Technology Convergence (ICTC)*. IEEE, 2017.
2. Ban, Byunghyun. "Mixed Reality Interface for Digital Twin of Plant Factory." *arXiv preprint arXiv:2211.00597* (2022).
3. Ban, Byunghyun, et al. "Nutrient solution management system for smart farms and plant factory." *2020 International Conference on Information and Communication Technology Convergence (ICTC)*. IEEE, 2020.
4. Ban, Byunghyun, Donghun Ryu, and Minwoo Lee. "Machine learning approach to remove ion interference effect in agricultural nutrient solutions." *2019 ICTC*. IEEE, 2019.
5. Ban, Byunghyun. "Deep learning method to remove chemical, kinetic and electric artifacts on ISEs." *2020 ICTC*. IEEE, 2020.
6. Ban, Byunghyun, Minwoo Lee, and Donghun Ryu. "ODE network model for nonlinear and complex agricultural nutrient solution system." *2019 ICTC*. IEEE, 2019.
7. Ban, Byunghyun. "Mathematical Model and Simulation for Nutrient-Plant Interaction Analysis." *2020 ICTC*. IEEE, 2020.
8. Yang, Si, et al. "Transfer learning from synthetic in-vitro soybean pods dataset for in-situ segmentation of on-branch soybean pods." *Proceedings of the IEEE/CVF CVPR*. 2022.
9. Wang, Bin, et al. "From species to cultivar: Soybean cultivar recognition using joint leaf image patterns by multiscale sliding chord matching." *Biosystems Engineering* 194 (2020): 99–111.
10. Abade, André da Silva, et al. "Nemanet: A convolutional neural network model for identification of nematodes soybean crop in brazil." *arXiv preprint arXiv:2103.03717* (2021).
11. Riera, Luis G., et al. "Deep multiview image fusion for soybean yield estimation in breeding applications." *Plant Phenomics* (2021).
12. Kentaro Wada. *Labelme: Image Polygonal Annotation with Python*. Version 5.2.1. https://github.com/wkentaro/labelme.
13. Reza, Ali M. "Realization of the contrast limited adaptive histogram equalization (CLAHE) for real-time image enhancement." *Journal of VLSI Signal Processing Systems* 38 (2004): 35–44. 