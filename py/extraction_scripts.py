from extraction import *

def reduce_standard_first_stage(image_file, bias_frame, normalized_flat, mask, px_thresh):
    
    image_data = copy.deepcopy(image_file[0].data)
    
    bias_subtracted_image = bias_subtract(image_data, bias_frame)
    
    image_variance = variance_image(bias_subtracted_image)
    
    normalized_image = flat_normalize_image(bias_subtracted_image, normalized_flat, mask)
    
    normalized_variance = flat_normalize_image(image_variance, normalized_flat, mask)
    
    masked_image = mask_image(normalized_image, mask)
    
    masked_variance = mask_image(normalized_variance, mask)
    
    poly_slit_model = slit_fit_model(masked_image)
    
    poly_slit_trace = slit_fit_trace(poly_slit_model)
    
    image_slices = gen_cent_slc(masked_image, poly_slit_trace, px_thresh)
    
    variance_slices = gen_cent_slc(masked_variance, poly_slit_trace, px_thresh)
    
    spatial_profile = create_norm_spatial_profile(image_slices)
    
    return image_slices, variance_slices, poly_slit_model, spatial_profile
    
def reduce_science_first_stage(image_file, bias_frame, normalized_flat, mask, px_thresh, poly_slit_model):
    
    image_data = copy.deepcopy(image_file[0].data)
    
    bias_subtracted_image = bias_subtract(image_data, bias_frame)
    
    print("Subtracted Bias")
    
    image_variance = variance_image(bias_subtracted_image)
    
    normalized_image = flat_normalize_image(bias_subtracted_image, normalized_flat, mask)
    
    normalized_variance = flat_normalize_image(image_variance, normalized_flat, mask)
    
    masked_image = mask_image(normalized_image, mask)
    
    masked_variance = mask_image(normalized_variance, mask)
    
    poly_slit_trace = slit_fit_trace(poly_slit_model)
    
    image_slices = gen_cent_slc(masked_image, poly_slit_trace, px_thresh)
    
    poly_shift = slit_fit_shift(image_slices, poly_slit_model, px_thresh)
    
    shifted_poly = slit_fit_trace(poly_shift)
    
    centered_slices = gen_cent_slc(masked_image, shifted_poly, px_thresh)
    
    variance_slices = gen_cent_slc(masked_variance, shifted_poly, px_thresh)
    
    spatial_profile = create_norm_spatial_profile(centered_slices)
    
    return centered_slices, variance_slices, spatial_profile

def reduce_second_stage(image_slices, variance_slices, spatial_profile, bkg_percent_thresh):
    
    bsubtracted_image_slices, background_spec = background_subtract(image_slices, spatial_profile, bkg_percent_thresh)
    
    bsubtracted_variance_slices, vbackground_spec = background_subtract(variance_slices, spatial_profile, bkg_percent_thresh)
    
    extraction_weight = weight_function(bsubtracted_image_slices)
    
    spect = extract_spectrum(bsubtracted_image_slices, extraction_weight)
    
    variance = extract_variance(bsubtracted_variance_slices, extraction_weight)
    
    return spect, variance, background_spec