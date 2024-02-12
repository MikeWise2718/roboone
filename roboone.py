

class RobotOne:

    def __init__(self)
        pass

    def DefineRobotBase(self, stage, cell, ridx, rptoff, rhomeang):
        gprim = cell["prim"]
        pname = gprim.GetPrim().GetPath()
        robbase = copy.deepcopy(self.typedict["robb"])
        oname = f"{pname}/robotbase{ridx}"
        robbase["prim_name"] = oname
        robbase["tag_name"] = f"robotbase{ridx}"

        self.AddEntityToDict(robbase, cell)

        oprim = UsdGeom.Xform.Define(stage, oname)
        oprim.AddTranslateOp().Set(rptoff)
        if self.tmax==0:
            oprim.AddRotateYOp().Set(rhomeang)
        else:
            rot = oprim.AddRotateYOp()
            rot.Set(time=0, value=rhomeang)
            rot.Set(time=self.clipmax/2, value=rhomeang+180)
            rot.Set(time=self.clipmax, value=rhomeang)
        otag = f"robotbase{ridx}"
        robbase["prim"] = oprim  # save the prim for later use
        robbase["tag_name"] = otag
        robbase["ctrl_tag"] = otag

        (dx, dy, dz) = robbase["dim"]
        rx = robbase["rx"]
        ry = robbase["ry"]
        rz = robbase["rz"]

        (fprim, _) = DefinePrimFromString(stage, f"{oname}/cyl", "cyl")
        fprim.AddScaleOp().Set((dx/2, dy/2, dz/2))
        fprim.AddRotateXOp().Set(90)
        fprim.GetDisplayColorAttr().Set(robbase["color"])
        SetUsdPrimAttrInt(oprim, "deb:robot_idx", ridx)
        SetUsdPrimAttrFloat(oprim, "deb:robot_x", rptoff[0])
        SetUsdPrimAttrFloat(oprim, "deb:robot_z", rptoff[2])
        SetUsdPrimAttrFloat(oprim, "deb:robot_width_dz", dz)
        SetUsdPrimAttrFloat(oprim, "deb:robot_length_dx", dx)
        SetUsdPrimAttrFloat(oprim, "deb:robot_height_dy", dy)

        jointoff = (0,dy/2,0)
        self.DefineRobotJoint(stage, robbase, 1, jointoff, rx,ry,rz, 1)

    def DefineRobotJoint(self, stage, robpar, ridx, joff, angx, angy, angz, lev):
        gprim = robpar["prim"]
        pname = gprim.GetPrim().GetPath()
        joint = copy.deepcopy(self.typedict["robj"])
        oname = f"{pname}/joint{lev}"
        joint["prim_name"] = oname
        joint["tag_name"] = f"joint{lev}"
        (dx, dy, dz) = joint["dim"]
        rx = joint["rx"]
        ry = joint["ry"]
        rz = joint["rz"]

        if lev==0:
            rx *= 3


        self.AddEntityToDict(joint, robpar)

        oprim = UsdGeom.Xform.Define(stage, oname)
        joff = (joff[0], joff[1], joff[2])
        oprim.AddTranslateOp().Set(joff)
        oname2 = f"{pname}/joint{lev}/rot"
        oprim2 = UsdGeom.Xform.Define(stage, oname2)

        if rx!=0:
            oprim2.AddRotateXOp().Set(rx)
        if ry!=0:
            oprim2.AddRotateYOp().Set(ry)
        if rz!=0:
            oprim2.AddRotateZOp().Set(rz)

        otag = f"joint{lev}"
        joint["prim"] = oprim2  # save the prim for later use
        joint["tag_name"] = otag
        joint["ctrl_tag"] = otag

 
        (fprim, _) = DefinePrimFromString(stage, f"{oname2}/cyl", "cyl")
        foff = (0, dy/2, 0)
        fprim.AddTranslateOp().Set(foff)
        fprim.AddScaleOp().Set((dx/2, dy/2, dz/2))
        fprim.AddRotateXOp().Set(90)
        fprim.GetDisplayColorAttr().Set(joint["color"])
        SetUsdPrimAttrInt(oprim, "deb:robot_idx", ridx)
        SetUsdPrimAttrInt(oprim, "deb:robot_lev", lev)
        SetUsdPrimAttrFloat(oprim, "deb:robot_x", joff[0])
        SetUsdPrimAttrFloat(oprim, "deb:robot_z", joff[2])
        SetUsdPrimAttrFloat(oprim, "deb:robot_width_dz", dz)
        SetUsdPrimAttrFloat(oprim, "deb:robot_length_dx", dx)
        SetUsdPrimAttrFloat(oprim, "deb:robot_height_dy", dy)

        if lev>0:
            joff = (0,dy,0)
            self.DefineRobotJoint(stage, joint, 1, joff, angx, angy, angz, lev-1)
