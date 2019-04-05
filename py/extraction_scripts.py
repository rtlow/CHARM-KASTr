from extraction import *

def reduce_standard_first_stage(image_file, bias_frame, normalized_flat, mask, px_thresh):
    
    print("Reduction Ho!")
    image_data = copy.deepcopy(image_file[0].data)
    print("Loaded image")
    bias_subtracted_image = bias_subtract(image_data, bias_frame)
    print("Subtracted Bias")
    image_variance = variance_image(bias_subtracted_image)
    print("Calculated Variance")
    normalized_image = flat_normalize_image(bias_subtracted_image, normalized_flat, mask)
    print("Flat Field Corrected the image")
    normalized_variance = flat_normalize_image(image_variance, normalized_flat, mask)
    print("Flat Field Corrected the variance")
    masked_image = mask_image(normalized_image, mask)
    print("Masked the image")
    masked_variance = mask_image(normalized_variance, mask)
    print("Masked the variance")
    poly_slit_model = slit_fit_model(masked_image)
    print("Created the slit trace")
    poly_slit_trace = slit_fit_trace(poly_slit_model)
    
    image_slices = gen_cent_slc(masked_image, poly_slit_trace, px_thresh)
    print("Generated Centered Image Slices")
    variance_slices = gen_cent_slc(masked_variance, poly_slit_trace, px_thresh)
    print("Generated Centered Variance SLices")
    spatial_profile = create_norm_spatial_profile(image_slices)
    print("Created spatial profile")
    return image_slices, variance_slices, poly_slit_model, spatial_profile
    
def reduce_science_first_stage(image_file, bias_frame, normalized_flat, mask, px_thresh, poly_slit_model):
    
    print("Reduction Ho!")
    image_data = copy.deepcopy(image_file[0].data)
    print("Loaded image")
    bias_subtracted_image = bias_subtract(image_data, bias_frame)
    print("Subtracted Bias")
    image_variance = variance_image(bias_subtracted_image)
    print("Calculated Variance")
    normalized_image = flat_normalize_image(bias_subtracted_image, normalized_flat, mask)
    print("Flat Field Corrected the image")
    normalized_variance = flat_normalize_image(image_variance, normalized_flat, mask)
    print("Flat Field Corrected the variance")
    masked_image = mask_image(normalized_image, mask)
    print("Masked the image")
    masked_variance = mask_image(normalized_variance, mask)
    print("Masked the variance")
    
    poly_slit_trace = slit_fit_trace(poly_slit_model)
    
    image_slices = gen_cent_slc(masked_image, poly_slit_trace, px_thresh)
    print("Generated Centered Image Slices")
    
    spatial_profile = create_norm_spatial_profile(image_slices)
    poly_shift = slit_fit_shift(image_slices, poly_slit_model, spatial_profile, px_thresh)
    print("Shifted the slit fit")
    shifted_poly = slit_fit_trace(poly_shift)
    
    centered_slices = gen_cent_slc(masked_image, shifted_poly, px_thresh)
    print("Generated Centered Image Slices")
    variance_slices = gen_cent_slc(masked_variance, shifted_poly, px_thresh)
    print("Generated Centered Variance SLices")
    shisfted_profile = create_norm_spatial_profile(centered_slices)
    print("Created spatial profile")
    return centered_slices, variance_slices, spatial_profile

def reduce_second_stage(image_slices, variance_slices, spatial_profile, bkg_percent_thresh):
    
    print("Reduction Continue!")
    bsubtracted_image_slices, background_spec = background_subtract(image_slices, spatial_profile, bkg_percent_thresh)
    print("Subtracted the background from image")
    bsubtracted_variance_slices, vbackground_spec = background_subtract(variance_slices, spatial_profile, bkg_percent_thresh)
    print("Subtracted the background from variance")
    extraction_weight = weight_function(bsubtracted_image_slices)
    print("Generated the spectral weighting function")
    spect = extract_spectrum(bsubtracted_image_slices, extraction_weight)
    print("Extracted the spectrum")
    variance = extract_variance(bsubtracted_variance_slices, extraction_weight)
    print("Extracted the variance")
    return spect, variance, background_spec