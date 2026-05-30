function rotate_inplace_cropped(img, angle_degrees, bg_color=RGB(0, 0, 0))
    center = [mean(axes(img, 1)), mean(axes(img, 2))]

    θ = deg2rad(angle_degrees)
    tfm = Translation(center...) ∘ LinearMap(RotMatrix(θ)) ∘ Translation((-center)...)

    img_rotated = warp(img, tfm, axes(img), fillvalue=bg_color)

    return img_rotated
end